import typing as t
import argparse
from importlib import import_module
from types import ModuleType
from . import TargetFunction, ContFunction, ArgumentParser


def setup_module() -> "_FakeModule":
    return _FakeModule()


def setup_for_multi_command(
    fn: TargetFunction,
) -> t.Tuple["M", ArgumentParser, ContFunction]:
    parser = argparse.ArgumentParser()  # xxx
    parser.print_usage = parser.print_help

    def cont(*, params: t.Dict[str, t.Any]):

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
