from typing import List, Union

from pytest_soft_asserts.libassert import Assert
from pytest_soft_asserts.table.row import Column


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
