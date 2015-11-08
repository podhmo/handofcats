# -*- coding:utf-8 -*-
import argparse
import logging
logger = logging.getLogger(__name__)


class WrappedArgumentParser(object):
    def __init__(self, parser, positionals, optionals):
        self.parser = parser
        self.positionals = positionals
        self.optionals = optionals
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def __getattr__(self, k):
        return getattr(self.parser, k)

    def parse_args(self, args):
        args = self.parser.parse_args(args)
        for callback in self.callbacks:
            result = callback(args)
            if result is not None:
                args = result
        return args


class ArgumentParserCreator(object):
    def __init__(self, argspec, help_dict=None, description=None):
        self.argspec = argspec
        self.len_of_opts = len(self.argspec.defaults or [])
        self.help_dict = help_dict or {}
        self.description = description or ""
        self._positionals = []
        self._optionals = []

    def get_option_format(self, name):
        return name.strip("_").replace("_", "-")

    def add_optional(self, parser, name, default):
        help = self.help_dict.get(name)
        self._optionals.append(name)
        if default is True:
            parser.add_argument("--{}".format(self.get_option_format(name)),
                                action="store_false",
                                help=help,
                                dest=name)
        elif default is False:
            parser.add_argument("--{}".format(self.get_option_format(name)),
                                action="store_true",
                                help=help,
                                dest=name)
        elif isinstance(default,
                        int):
            parser.add_argument("--{}".format(self.get_option_format(name)),
                                type=int,
                                default=default,
                                help=help,
                                dest=name)
        elif isinstance(default,
                        float):
            parser.add_argument("--{}".format(self.get_option_format(name)),
                                type=float,
                                default=default,
                                help=help,
                                dest=name)
        else:
            parser.add_argument("--{}".format(self.get_option_format(name)),
                                default=default,
                                help=help,
                                dest=name)

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

    def create_parser(self, prog=None):
        parser = argparse.ArgumentParser(prog=prog, description=self.description)
        for k, v in self.iterate_optionals():
            self.add_optional(parser, k, v)

        for arg in self.iterate_positionals():
            self.add_positional(parser, arg)
        return WrappedArgumentParser(parser, self._positionals, self._optionals)
    __call__ = create_parser
