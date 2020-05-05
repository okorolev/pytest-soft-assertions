from dataclasses import dataclass, field
from typing import Any, List, Union

from pytest_soft_asserts.libassert import Assert


@dataclass
class Column:
    value: Any
    condition: Union[str, object] = None
    skip_type: bool = field(default=False)
    skip_condition: bool = field(default=False)

    @property
    def data(self) -> str:
        value = self.value
        condition = self.condition

        if self.skip_type:
            if not condition:
                return f'{value}'

            return f'{condition} {value}'

        if self.skip_condition:
            return f'{value}'

        return f'{condition} {value}'


def typed_column(column: Column) -> str:
    return column.data


def to_row(data: Assert) -> List[Union[str, Column]]:
    left = data.left
    right = data.right
    is_left_only = data.left_only
    condition = data.condition
    expression = data.pretty_code

    if condition in ['is', '==']:
        current_value = Column(value=left, skip_condition=True)
        expected = Column(condition=condition, value=right, skip_condition=True)

    elif is_left_only or condition in ['not', 'or']:
        condition = '<Not condition>' if is_left_only else condition
        current_value = Column(value=left, skip_condition=True)
        expected = Column(value='<Not None>', skip_type=True)

    else:
        current_value = Column(value=left, skip_condition=True)
        expected = Column(condition=condition, value=right)

    return [str(expression), str(condition), current_value, expected]
