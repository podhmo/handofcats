import typing as t
import argparse
import magicalimport
from handofcats import get_default_multi_driver
from types import ModuleType
from .types import TargetFunction
from logging import getLogger as get_logger

logger = get_logger(__name__)


def _import_symbol(path, sep=":", logger=logger) -> TargetFunction:
    try:
        val = magicalimport.import_symbol(path, sep=sep, cwd=True)
        assert callable(val)
        return t.cast(TargetFunction, val)
    except (ImportError, AttributeError) as e:
        logger.info(str(e), exc_info=True)
        raise argparse.ArgumentTypeError(f"""\x1b[33m{e}\x1b[0m""")


def _import_module(path, logger=logger) -> ModuleType:
    try:
        return magicalimport.import_module(path, cwd=True)
    except ImportError as e:
        logger.info(str(e), exc_info=True)
        raise argparse.ArgumentTypeError(f"""\x1b[33m{e}\x1b[0m""")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="handofcats", add_help=False)
    parser.print_usage = parser.print_help

    parser.add_argument(
        "entry_point",
        help="target EntryPoint. (format '<file name>:<attr>' or '<file name>')",
    )
    parser.add_argument(
        "--driver",
        type=_import_symbol,
        default="handofcats.driver:Driver",
        help="DI, driver class, this is experimental (default: handofcats.driver:Driver)",
    )
    parser.add_argument(
        "--multi-driver",
        type=_import_symbol,
        default="handofcats.driver:MultiDriver",
        help="DI, multidriver class, this is experimental (default: handofcats.driver:MultiDriver)",
    )

    args, rest_argv = parser.parse_known_args(argv)

    attr = None
    if ":" in args.entry_point:
        module_path, attr = args.entry_point.rsplit(":", 1)
    else:
        module_path = args.entry_point

    module = magicalimport.import_module(module_path, cwd=True)

    # as single command
    if attr is not None:
        fn = getattr(module, attr)
        driver = args.driver(fn)
        return driver.run(rest_argv)

    # as multi command
    driver = get_default_multi_driver()
    assert isinstance(driver, args.multi_driver)
    if driver is not None:
        return driver.run(rest_argv)

    fns = _collect_functions(module)
    driver = args.multi_driver(fns)
    return driver.run(rest_argv)


def _collect_functions(module: ModuleType) -> t.List[TargetFunction]:
    functions: t.List[TargetFunction] = []
    for name, val in module.__dict__.items():
        if name.startswith("_"):
            continue
        elif not callable(val):
            continue
        elif val.__module__ != module.__name__:
            continue
        functions.append(val)
    return functions


if __name__ == "__main__":
    main()