import ast

import astor
from pytest_ast_transformer.transformer import PytestTransformer

from pytest_soft_asserts.exceptions import NotSupportedAstNode
from pytest_soft_asserts.libassert import SoftAssertions


class AssertTransformer(PytestTransformer):
    context = {
        'SoftAssertions': SoftAssertions,
    }

    def visit_Assert(self, node: ast.Assert) -> ast.AST:
        source = astor.to_source(node.test)
        keywords = [
            ast.keyword(arg='result', value=ast.Name(id=source)),
        ]

        if isinstance(node.test, ast.Compare):
            keywords.extend([
                ast.keyword(arg='condition', value=get_op(node.test.ops[0])),
                ast.keyword(arg='left', value=node.test.left),
                ast.keyword(arg='right', value=node.test.comparators[0]),
            ])

        elif isinstance(node.test, ast.BoolOp):
            keywords.extend([
                ast.keyword(arg='condition', value=get_op(node.test.op)),
                ast.keyword(arg='left', value=node.test.values[0]),
                ast.keyword(arg='right', value=node.test.values[1]),
            ])

        elif isinstance(node.test, ast.UnaryOp):
            keywords.extend([
                ast.keyword(arg='condition', value=get_op(node.test.op)),
                ast.keyword(arg='left', value=node.test.operand),
            ])

        else:
            keywords.extend([
                ast.keyword(arg='left', value=node.test),
            ])

        # call ctx.assert_(...)
        assert_line = ast.Str(s=source)
        assert_ctx = ast.Attribute(value=ast.Name(id='ctx', ctx=ast.Load()), attr='assert_', ctx=ast.Load())
        call_func = ast.Call(func=assert_ctx, args=[assert_line], keywords=keywords)
        expr = ast.Expr(value=call_func)

        return fix_node(expr)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        with_item = ast.withitem(
            context_expr=ast.Call(func=ast.Name(id='SoftAssertions', ctx=ast.Load()), args=[], keywords=[]),
            optional_vars=ast.Name(id='ctx', ctx=ast.Store())
        )
        with_stmt = ast.With(items=[with_item], body=node.body)

        node.body = [with_stmt]
        new_node = fix_node(node)

        return self.generic_visit(new_node)


def fix_node(node: ast.AST) -> ast.AST:
    """ Hack for fix line numbers
    """
    new_node = ast.parse(astor.to_source(node))
    new_node = new_node.body[0]  # type: ignore
    return new_node


def get_op(cls: ast.AST) -> ast.Str:
    ops = {
        ast.Is: 'is',
        ast.Not: 'not',
        ast.IsNot: 'is not',
        ast.In: 'in',
        ast.NotIn: 'not in',
        ast.NotEq: '!=',
        ast.Eq: '==',
        ast.Gt: '>',
        ast.Lt: '<',
        ast.GtE: '>=',
        ast.LtE: '<=',
        ast.Or: 'or',
    }
    op = ops.get(cls.__class__)

    if not op:
        raise NotSupportedAstNode(f'AST node not supported: {cls.__class__}')

    return ast.Str(s=op)
