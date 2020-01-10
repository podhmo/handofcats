import typing as t
import argparse
from importlib import import_module
from types import ModuleType
from . import TargetFunction, ContFunction, ArgumentParser


def setup(fn: TargetFunction,) -> t.Tuple["M", ArgumentParser, ContFunction]:
    parser = argparse.ArgumentParser(prog=fn.__name__, description=fn.__doc__)
    parser.print_usage = parser.print_help

    parser.add_argument("--expose", action="store_true")  # xxx (for ./expose.py)
    parser.add_argument("--inplace", action="store_true")  # xxx (for ./expose.py)
    parser.add_argument("--typed", action="store_true")  # xxx (for ./expose.py)

    def cont(*, params: t.Dict[str, t.Any]):
        params.pop("expose", None)  # xxx: for ./expose.py
        params.pop("inplace", None)  # xxx: for ./expose.py
        params.pop("typed", None)  # xxx: for ./expose.py
        return fn(**params)

    return _FakeModule(), parser, cont


def setup_for_multi_command(fn: TargetFunction) -> t.Tuple["M", ArgumentParser, ContFunction]:
    parser = argparse.ArgumentParser()  # xxx
    parser.print_usage = parser.print_help

    parser.add_argument("--expose", action="store_true")  # xxx (for ./expose.py)
    parser.add_argument("--inplace", action="store_true")  # xxx (for ./expose.py)
    parser.add_argument("--typed", action="store_true")  # xxx (for ./expose.py)

    def cont(*, params: t.Dict[str, t.Any]):
        params.pop("expose", None)  # xxx: for ./expose.py
        params.pop("inplace", None)  # xxx: for ./expose.py
        params.pop("typed", None)  # xxx: for ./expose.py

        subcommand = params.pop("subcommand")  # xxx
        return subcommand(**params)  # xxx

    return _FakeModule(), parser, cont


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
