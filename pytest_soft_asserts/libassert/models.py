from dataclasses import dataclass
from typing import Union


NOT_SET = object()


@dataclass
class Assert:
    code: str
    result: bool
    left: object
    right: object
    condition: Union[str, object]

    @property
    def left_only(self) -> bool:
        have_left = self.left is not NOT_SET
        no_right = self.right is NOT_SET
        no_condition = self.condition is NOT_SET

        return have_left and no_right and no_condition

    @property
    def pretty_code(self) -> str:
        code = self.code.replace('\n', '')
        code_without_phs = code[1:-1]

        return f'assert {code if self.left_only else code_without_phs}'

    @property
    def is_failed(self) -> bool:
        return not self.result
