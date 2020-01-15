import typing as t
import contextlib
from importlib import import_module
from types import ModuleType


class _Helper:
    def is_(self, x: t.Any, y: t.Any) -> bool:
        return x is y

    def is_not(self, x: t.Any, y: t.Any) -> bool:
        return x is not y

    def in_(self, x: t.Any, y: t.Any) -> bool:
        return x in y

    def or_(self, x: t.Any, y: t.Any) -> bool:
        return x or y

    def format_(self, fmt: str, *args, **kwargs) -> str:
        return fmt.format(*args, **kwargs)


class _FakeModule(_Helper):
    """fake _codeobject.Module. no effect"""

    def import_(self, name) -> ModuleType:
        return import_module(name)

    def let(self, name: str, ob: t.Any) -> t.Any:
        return ob

    def stmt(self, ob: t.Any) -> t.Any:
        return ob

    @contextlib.contextmanager
    def if_(self, cond: bool) -> None:
        if not cond:
            raise Fail(cond)
        yield None

    def sep(self):
        pass

    def return_(self, ob: t.Any) -> t.Any:
        return ob

    def symbol(self, ob: t.Any) -> t.Any:
        return ob

    def constant(self, ob: str) -> str:
        return ob

    def setattr(self, ob: t.Any, name: str, val: t.Any) -> None:
        setattr(ob, name, val)

    def getattr(self, ob: t.Any, name: str) -> t.Optional[t.Any]:
        return getattr(ob, name)

    def unnewline(self) -> None:
        pass


class Fail(Exception):
    pass
