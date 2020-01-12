import typing as t
import sys
from .driver import Driver, MultiDriver
from .types import TargetFunction
from .config import Config, default_config


def import_symbol_maybe(ob_or_path: str, *, sep: str = ":") -> t.Optional[t.Any]:
    from magicalimport import import_symbol

    if not isinstance(ob_or_path, str):
        return ob_or_path
    return import_symbol(ob_or_path, sep=sep, cwd=True)


def as_command(
    fn=None,
    *,
    argv=None,
    driver=Driver,
    level=2,
    _force=False,
    config: Config = default_config,
) -> TargetFunction:
    create_driver = import_symbol_maybe(driver)
    if argv is None:
        argv = sys.argv[1:]

    def call(fn, level=1, argv=argv):
        if not _force:
            # caller module extraction, if it is __main__, calling as command
            frame = sys._getframe(level)
            name = frame.f_globals["__name__"]
            if name != "__main__":
                return fn
        driver = create_driver(fn, config=config)
        return driver.run(argv)

    if fn is None:
        return call
    else:
        return call(fn, level=level, argv=argv)


_default_multi_driver = None


def as_subcommand(fn: TargetFunction, *, driver=MultiDriver) -> TargetFunction:
    global _default_multi_driver
    if _default_multi_driver is None:
        create_driver = import_symbol_maybe(driver)
        _default_multi_driver = create_driver()
    _default_multi_driver.register(fn)
    return fn


def _as_subcommand_run(
    argv=None, *, level=1, _force=False, config: t.Optional[Config] = None,
):
    global _default_multi_driver

    if _default_multi_driver is None:
        raise RuntimeError("please register functions by as_subcommand()")

    driver = _default_multi_driver
    if config is not None:
        _default_multi_driver.config = config

    if argv is None:
        argv = sys.argv[1:]

    if not _force:
        # caller module extraction, if it is __main__, calling as command
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name != "__main__":
            return
    return driver.run(argv)


def get_default_multi_driver() -> t.Optional[MultiDriver]:
    global _default_multi_driver
    return _default_multi_driver


as_subcommand.run = _as_subcommand_run  # noqa


# alias (TODO: remove)
handofcats = as_command
