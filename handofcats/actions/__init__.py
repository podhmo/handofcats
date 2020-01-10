import typing as t
import typing_extensions as tx


TargetFunction = t.Callable[..., t.Any]
ContFunction = t.Callable[..., t.Any]


class ArgumentParser(tx.Protocol):
    # TODO: typing
    def parse_args(self, *args, **kwargs):
        ...

    def add_argument(self, *args, **kwargs):
        ...
