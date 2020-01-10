import typing as t
from importlib import import_module
from types import ModuleType
from . import TargetFunction, ArgumentParser


def setup_module() -> "_FakeModule":
    return _FakeModule()


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
