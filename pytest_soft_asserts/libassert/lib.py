from dataclasses import dataclass, field
from typing import List

from texttable import Texttable

from pytest_soft_asserts.libassert.models import NOT_SET, Assert
from pytest_soft_asserts.table import to_row, typed_column


@dataclass
class SoftAssertions:
    assertions: List[Assert] = field(default_factory=list)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_failed:
            raise AssertionError(f'\n{self.draw_results()}')

    def assert_(self, code: str, result: bool, left=NOT_SET, right=NOT_SET, condition=NOT_SET) -> None:
        self.assertions.append(
            Assert(
                code=code,
                left=left,
                right=right,
                result=result,
                condition=condition,
            )
        )

    @property
    def is_failed(self) -> bool:
        return any(_assert.is_failed for _assert in self.assertions)

    def draw_results(self) -> str:
        rows_generator = (to_row(_assert) for _assert in self.assertions if _assert.is_failed)

        table = Texttable()
        table.header(['expression', 'condition', 'current value', 'expected'])
        table.set_cols_dtype([
            'a',  # auto type
            'a',  # auto type
            typed_column,
            typed_column,
        ])
        table.add_rows(rows_generator, header=False)

        return table.draw()
