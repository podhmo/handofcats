# -*- coding:utf-8 -*-
import re
import inspect
import sys
import argparse


class CommandFromFunction(object):
    def __init__(self, fn, argspec, help_dict=None, description=None):
        self.fn = fn
        self.argspec = argspec
        self.len_of_opts = len(self.argspec.defaults or [])
        self.positionals = []
        self.name = self.fn.__name__
        self.help_dict = help_dict or {}
        self.parser = self.create_parser(description)

    def _add_optional(self, parser, name, default):
        help = self.help_dict.get(name)
        if default is True:
            parser.add_argument("--{}".format(name), action="store_false", help=help)
        elif default is False:
            parser.add_argument("--{}".format(name), action="store_true", help=help)
        else:
            parser.add_argument("--{}".format(name), default=default, help=help)

    def _add_positional(self, parser, name):
        help = self.help_dict.get(name)
        self.positionals.append(name)
        parser.add_argument(name, help=help)

    def _iterate_positionals(self):
        if self.argspec.defaults is None:
            return self.argspec.args
        else:
            return self.argspec.args[:-self.len_of_opts]

    def _iterate_optionals(self):
        if self.argspec.defaults is None:
            return []
        else:
            return zip(self.argspec.args[-self.len_of_opts:], self.argspec.defaults)

    def create_parser(self, description):
        parser = argparse.ArgumentParser(description=description)
        for k, v in self._iterate_optionals():
            self._add_optional(parser, k, v)

        for arg in self._iterate_positionals():
            self._add_positional(parser, arg)
        return parser

    def activate(self, level=1):
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name == "__main__":
            return self(sys.argv[1:])
        else:
            return self.fn

    def __call__(self, args):
        parser = self.parser
        try:
            parsed = parser.parse_args(args)
            args = [getattr(parsed, name) for name in self.positionals]
            kwargs = {name: getattr(parsed, name) for name, _ in self._iterate_optionals()}
            self.fn(*args, **kwargs)
        except:
            sys.exit(-1)


def get_help_dict(doc):
    d = {}
    rx = re.compile("^ *:param +(?P<param>\w+): +(?P<doc>.+) *$", re.M)
    d.update({name: doc for name, doc in rx.findall(doc)})
    rx = re.compile("^ *:param +(?P<type>\w+) +(?P<param>\w+): +(?P<doc>.+) *$", re.M)
    d.update({name: doc for type_, name, doc in rx.findall(doc)})
    return d


def get_description(doc):
    r = []
    for line in doc.split("\n"):
        line = line.strip()
        if line and not line.startswith(":"):
            r.append(line)
    return "\n".join(r)


def as_command(fn):
    argspec = inspect.getargspec(fn)
    doc = fn.__doc__ or ""
    help_dict = get_help_dict(doc)
    description = get_description(doc)
    return CommandFromFunction(fn, argspec, help_dict, description).activate(level=2)

# alias
handofcats = as_command
