import sys
from .driver import Driver
from .util import import_symbol


def import_symbol_maybe(ob_or_path, sep=":"):
    if not isinstance(ob_or_path, str):
        return ob_or_path
    return import_symbol(ob_or_path, sep=sep)


def as_command(fn=None, argv=None, driver=Driver, level=2, _force=False):
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
        driver = create_driver()
        return driver.run(fn, argv)

    if fn is None:
        return call
    else:
        return call(fn, level=level, argv=argv)


# alias
handofcats = as_command
