import ast

import astor

from pytest_soft_asserts.exceptions import NotSupportedAstNode


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
