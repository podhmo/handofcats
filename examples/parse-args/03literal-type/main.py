from handofcats import as_command
import typing as t
from typing_extensions import Literal

Mode = Literal["a", "w", "r"]
Value = Literal[0, 1, -1]


@as_command
def run(filename: str, *, mode: t.Optional[Mode] = "r", value: Value) -> None:
    pass
