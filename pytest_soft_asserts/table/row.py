from dataclasses import dataclass, field
from typing import Any, Union


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
