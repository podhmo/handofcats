import typing as t
import typing_extensions as tx

# TODO: document


T = t.TypeVar("T")
PrestringModule = t.Any


class ArgumentParser(tx.Protocol):
    # TODO: typing
    def parse_args(self, *args, **kwargs):
        ...

    def add_argument(self, *args, **kwargs):
        ...


TargetFunction = t.Callable[..., t.Any]


CustomizeActivateFunction = t.Callable[[t.Dict[str, t.Any]], None]
CustomizeSetupFunction = t.Callable[[ArgumentParser], CustomizeActivateFunction]


class SetupParserFunction(tx.Protocol[T]):
    def __call__(
        m: PrestringModule,
        fn_or_functions: T,
        argv=None,
        *,
        customizations: t.Optional[t.List[CustomizeSetupFunction]] = None,
    ) -> t.Tuple[ArgumentParser, t.List[CustomizeActivateFunction]]:
        ...
