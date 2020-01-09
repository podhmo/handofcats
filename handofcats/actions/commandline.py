import typing as t
import argparse
from importlib import import_module
from types import ModuleType
from . import TargetFunction, ContFunction, ArgumentParser


def setup(
    fn: TargetFunction, *, prog: t.Optional[str], description: t.Optional[str] = None
) -> t.Tuple["M", ArgumentParser, ContFunction]:
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.print_usage = parser.print_help
    return M(), parser, fn


class M:
    def import_(self, name) -> ModuleType:
        return import_module(name)

    def let(self, name: str, ob: t.Any) -> t.Any:
        return ob

    def stmt(self, ob: t.Any) -> t.Any:
        return ob

    def sep(self):
        return None

    def return_(self, ob: t.Any) -> t.Any:
        return ob

    def symbol(self, ob: t.Any) -> t.Any:
        return ob

    def setattr(self, ob: t.Any, name: str, val: t.Any) -> None:
        setattr(ob, name, val)

    def getattr(self, ob: t.Any, name: str) -> t.Optional[t.Any]:
        return getattr(ob, name)
