import sys
import re
import inspect
import functools
from prestring.python import (
    Module,
    LazyArgumentsAndKeywords,
)
from ._callback import CallbackArgumentParser


class _UnRepr:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

    __str__ = __repr__


def print_argparse_code(fn, history):
    def _make_args(history, default=""):
        name = history["name"]
        if name == "__init__":
            name = default
        kwargs = {k: (repr(v) if k != "type" else v.__name__) for k, v in history["kwargs"].items()}
        args = [repr(v) for v in history["args"]]
        return f"{name}({LazyArgumentsAndKeywords(args, kwargs)})"

    m = Module()
    with m.def_("main", "argv=None"):
        m.import_("argparse")
        m.stmt(f"parser = argparse.ArgumentParser{_make_args(history[0])}")
        m.stmt("parser.print_usage = parser.print_help")
        for x in history[1:-1]:
            m.stmt(f"parser.{_make_args(x)}")

        history[-1] = {
            "name": history[-1]["name"],
            "args": (_UnRepr("argv"), ),
            "kwargs": {},
        }  # xxx

        m.stmt(f"args = parser.{_make_args(history[-1])}")
        m.stmt(f"{fn.__name__}(**vars(args))")

    with m.if_("__name__ == '__main__'"):
        m.stmt("main()")

    with open(inspect.getsourcefile(fn)) as rf:
        source = rf.read()
    rx = re.compile("(?:^@([\S]+\.)?as_command.*|^.*import as_command.*)\n", re.MULTILINE)
    exposed = rx.sub("", "".join(source))
    print(exposed)
    print(m)
    sys.exit(0)


create_parser = functools.partial(CallbackArgumentParser, print_argparse_code)
