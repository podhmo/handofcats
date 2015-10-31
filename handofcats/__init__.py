# -*- coding:utf-8 -*-
import re
import inspect
import sys
import argparse
import logging
logger = logging.getLogger(__name__)


class WrappedArgumentParser(object):
    def __init__(self, parser, positionals, optionals):
        self.parser = parser
        self.positionals = positionals
        self.optionals = optionals

    def __getattr__(self, k):
        return getattr(self.parser, k)


class ParserCreator(object):
    def __init__(self, argspec, help_dict=None, description=None):
        self.argspec = argspec
        self.len_of_opts = len(self.argspec.defaults or [])
        self.help_dict = help_dict or {}
        self.description = description or ""
        self._positionals = []
        self._optionals = []

    def add_optional(self, parser, name, default):
        help = self.help_dict.get(name)
        self._optionals.append(name)
        if default is True:
            parser.add_argument("--{}".format(name), action="store_false", help=help)
        elif default is False:
            parser.add_argument("--{}".format(name), action="store_true", help=help)
        else:
            parser.add_argument("--{}".format(name), default=default, help=help)

    def add_positional(self, parser, name):
        help = self.help_dict.get(name)
        self._positionals.append(name)
        parser.add_argument(name, help=help)

    def iterate_positionals(self):
        if self.argspec.defaults is None:
            return self.argspec.args
        else:
            return self.argspec.args[:-self.len_of_opts]

    def iterate_optionals(self):
        if self.argspec.defaults is None:
            return []
        else:
            return zip(self.argspec.args[-self.len_of_opts:], self.argspec.defaults)

    def create_parser(self):
        parser = argparse.ArgumentParser(description=self.description)
        for k, v in self.iterate_optionals():
            self.add_optional(parser, k, v)

        for arg in self.iterate_positionals():
            self.add_positional(parser, arg)
        return WrappedArgumentParser(parser, self._positionals, self._optionals)
    __call__ = create_parser


class CommandFromFunction(object):
    _ParserCreator = ParserCreator

    def __init__(self, fn, argspec, help_dict=None, description=None):
        self.fn = fn
        self.parser_creator = self._ParserCreator(argspec, help_dict, description)

    def activate(self, level=1):
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name == "__main__":
            return self(sys.argv[1:])
        else:
            return self.fn

    def __call__(self, args):
        parser = self.parser_creator()
        try:
            parsed = parser.parse_args(args)
            args = [getattr(parsed, name) for name in parser.positionals]
            kwargs = {name: getattr(parsed, name) for name in parser.optionals}
        except Exception as e:
            sys.stderr.write("{!r}\n".format(e))
            logger.warning("error is occured", exc_info=True)
            sys.exit(-1)
        self.fn(*args, **kwargs)


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


def create_command_from_function(fn):
    argspec = inspect.getargspec(fn)
    doc = fn.__doc__ or ""
    help_dict = get_help_dict(doc)
    description = get_description(doc)
    return CommandFromFunction(fn, argspec, help_dict, description)


def as_command(fn):
    return create_command_from_function(fn).activate(level=2)

# alias
handofcats = as_command
