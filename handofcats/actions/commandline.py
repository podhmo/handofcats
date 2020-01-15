import typing as t
from ..types import TargetFunction, SetupParserFunction
from .. import customize
from ..config import Config, default_config
from ._fake import _FakeModule


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
        customizations.append(customize.logging_setup)

    parser, activate_functions = setup_parser(m, fn, customizations=customizations)
    args = parser.parse_args(argv)
    params = vars(args).copy()

    for activate in activate_functions:
        activate(params)
    return fn(**params)


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
        customizations.append(customize.logging_setup)

    parser, activate_functions = setup_parser(
        m, functions, customizations=customizations
    )
    args = parser.parse_args(argv)
    params = vars(args).copy()

    for activate in activate_functions:
        activate(params)

    subcommand = params.pop("subcommand")
    return subcommand(**params)
