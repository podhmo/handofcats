import typing as t
import dataclasses


def default_continuation(val: t.Optional[t.Any]) -> t.Any:
    # TODO: silence option?
    if val is not None:
        print(val)
    return val


@dataclasses.dataclass(frozen=True)
class Config:
    ignore_logging: bool = False
    ignore_expose: bool = False
    cont: t.Callable[[t.Any], t.Any] = default_continuation


default_config = Config()
