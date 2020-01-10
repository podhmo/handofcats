import typing as t
import typing_extensions as tx


TargetFunction = t.Callable[..., t.Any]


class ContFunction(tx.Protocol):
    def __call__(*, params: t.Dict[str, t.Any]) -> t.Any:
        ...


class ArgumentParser(tx.Protocol):
    # TODO: typing
    def parse_args(self, *args, **kwargs):
        ...

    def add_argument(self, *args, **kwargs):
        ...
