import typing

from pytest_soft_asserts.transformer import AssertTransformer


if typing.TYPE_CHECKING:
    from _pytest.config import Parser, Config
    from pytest_ast_transformer.ast_manager import ASTManager


def pytest_register_ast_transformer(ast_manager: 'ASTManager', config: 'Config'):
    if config.option.allow_soft_asserts:
        ast_manager.add_transformer(AssertTransformer())


def pytest_addoption(parser: 'Parser'):
    parser.addoption("--soft-asserts", action="store_true", dest="allow_soft_asserts", default=False)
