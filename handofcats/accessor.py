import typing as t
import inspect
from .util import reify
from collections import namedtuple


def option_name(name):
    return name.strip("_").replace("_", "-")


Option = namedtuple("Option", "name, option_name, required, type, default")


class Accessor:
    def __init__(self, fn):
        self.fn = fn

    @reify
    def resolver(self) -> "Resolver":
        return Resolver(self.fn)

    @reify
    def arguments(self) -> t.Sequence[Option]:
        r = []
        for name in self.resolver.argspec.args:
            if not self.resolver.has_default(name):
                r.append(self.create_positional(name))
        return r

    @reify
    def flags(self) -> t.Sequence[Option]:
        r = []
        for name in self.resolver.argspec.args:
            if self.resolver.has_default(name):
                r.append(self.create_flag(name, required=False))
        for name in self.resolver.argspec.kwonlyargs:
            required = not self.resolver.has_default(name)
            r.append(self.create_flag(name, required=required))
        return r

    def create_flag(self, name, *, required: bool = False) -> Option:
        return Option(
            name=name,
            option_name="{prefix}{name}".format(
                prefix="-" if len(name) <= 1 else "--", name=option_name(name)
            ),
            required=required,
            type=self.resolver.resolve_type(name),
            default=self.resolver.resolve_default(name),
        )

    def create_positional(self, name) -> Option:
        return Option(
            name=name,
            option_name=option_name(name).replace("-", "_"),
            required=True,
            type=self.resolver.resolve_type(name),
            default=self.resolver.resolve_default(name),
        )


def _getfullargspec(fn):
    argspec = inspect.getfullargspec(fn)
    if argspec.annotations is None:
        return argspec

    # XXX: for `from __future__ import annotations`
    annotations = t.get_type_hints(fn)
    assert len(argspec.annotations) == len(annotations)
    argspec.annotations.update(annotations)

    return argspec


class Resolver:
    def __init__(self, fn, *, argspec=None):
        self.fn = fn
        self.argspec = argspec or _getfullargspec(fn)

    @reify
    def _defaults(self) -> t.Dict[str, t.Any]:
        d = {}
        for i, v in enumerate(reversed(self.argspec.defaults or [])):
            k = self.argspec.args[-(i + 1)]  # 0 -> -1
            d[k] = v
        return d

    @reify
    def _kwonlydefaults(self) -> t.Dict[str, t.Any]:
        return self.argspec.kwonlydefaults or {}

    def has_default(self, name: str) -> bool:
        return name in self._kwonlydefaults or name in self._defaults

    def resolve_default(self, name: str) -> t.Optional[t.Any]:
        return self._kwonlydefaults.get(name) or self._defaults.get(name)

    def resolve_type(self, name: str) -> t.Optional[t.Type]:
        if self.argspec.annotations is None:
            return None
        return self.argspec.annotations.get(name)
