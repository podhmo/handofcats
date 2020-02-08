import typing as t
import dataclasses


@dataclasses.dataclass(frozen=True)
class Config:
    ignore_logging: bool = False
    ignore_expose: bool = False
    cont: t.Callable[[t.Any], t.Any] = print


default_config = Config()
