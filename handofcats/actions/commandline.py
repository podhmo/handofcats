import typing as t
from importlib import import_module
from types import ModuleType
from ..types import TargetFunction, SetupParserFunction
from .. import customize
from ..config import Config, default_config


class _FakeModule:
    """fake _codeobject.Module. no effect"""

    def import_(self, name) -> ModuleType:
        return import_module(name)

    def let(self, name: str, ob: t.Any) -> t.Any:
        return ob

    def stmt(self, ob: t.Any) -> t.Any:
        return ob

    def sep(self):
        pass

    def return_(self, ob: t.Any) -> t.Any:
        return ob

    def symbol(self, ob: t.Any) -> t.Any:
        return ob

    def setattr(self, ob: t.Any, name: str, val: t.Any) -> None:
        setattr(ob, name, val)

    def getattr(self, ob: t.Any, name: str) -> t.Optional[t.Any]:
        return getattr(ob, name)

    def unnewline(self) -> None:
        pass


def run_as_single_command(
    setup_parser: SetupParserFunction[TargetFunction],
    *,
    fn: TargetFunction,
    argv: t.Optional[str] = None,
    config: Config = default_config,
) -> t.Any:
    m = _FakeModule()

    customizations = []
    if not config.ignore_expose:
        customizations.append(customize.first_parser_setup)
    if not config.ignore_logging:
        # TODO: include generated code, emitted by `--expose`
        customizations.append(customize.logging_setup)

    parser, activate_functions = setup_parser(
        fn, m=m, customizations=customizations, config=config,
    )
    args = parser.parse_args(argv)
    params = vars(args).copy()

    for activate in activate_functions:
        activate(params)
    val = fn(**params)
    if val is None:
        return None
    return config.cont(val)


def run_as_multi_command(
    setup_parser: SetupParserFunction[t.List[TargetFunction]],
    *,
    functions: t.List[TargetFunction],
    argv: t.Optional[str] = None,
    config: Config = default_config,
) -> t.Any:
    m = _FakeModule()

    customizations = []
    if not config.ignore_expose:
        customizations.append(customize.first_parser_setup)
    if not config.ignore_logging:
        # TODO: include generated code, emitted by `--expose`
        customizations.append(customize.logging_setup)

    parser, activate_functions = setup_parser(
        functions, m=m, customizations=customizations, config=config,
    )
    args = parser.parse_args(argv)
    params = vars(args).copy()

    for activate in activate_functions:
        activate(params)

    subcommand = params.pop("subcommand")
    val = subcommand(**params)
    if val is None:
        return None
    return config.cont(val)
