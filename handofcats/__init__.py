import sys
from .driver import Driver


def import_symbol_maybe(ob_or_path, sep=":"):
    if not isinstance(ob_or_path, str):
        return ob_or_path
    return import_symbol_maybe(ob_or_path, sep=sep)


def as_command(fn=None, argv=None, driver=Driver, level=2):
    create_driver = import_symbol_maybe(driver)

    def call(fn, level=1, argv=argv):
        # caller module extraction, if it is __main__, calling as command
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name != "__main__":
            return fn
        driver = create_driver(fn)
        return driver.run()

    if fn is None:
        return call
    else:
        return call(fn, level=level, argv=argv)


# alias
handofcats = as_command
