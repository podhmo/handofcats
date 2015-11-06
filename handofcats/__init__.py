# -*- coding:utf-8 -*-
import re
import inspect
import sys
import argparse
from cached_property import cached_property as reify
import logging
from handofcats.compat import text_, bytes_
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


class CommandManager(object):
    def __init__(self):
        self.managed_set = set()

    def mark(self, target):
        self.managed_set.add(target)
        return target

    def is_marked(self, target):
        return target in self.managed_set

    def collect(self):
        return self.managed_set

    def get_module_and_pathlist(self, module_or_path, importer):
        if hasattr(module_or_path, "__path__"):
            return module_or_path, module_or_path.__path__
        else:
            module = importer(module_or_path)
            return module, module.__path__

    def scan(self, root, exclude=None):
        import glob
        import os.path
        from importlib import import_module

        logging.info("scan: %s", root)
        m, pathlist = self.get_module_and_pathlist(root, importer=import_module)
        root_package = m.__package__ or m.__name__
        for path in pathlist:
            logging.debug("scan path: %s", path)
            for target in glob.glob(os.path.join(path, "*.py")):
                if target.endswith("/__init__.py"):
                    target = target.replace("/__init__.py", "")
                if target == path:
                    continue
                if exclude and exclude(target):
                    continue
                logger.debug("scan target: %s", target)
                if target.endswith(".py"):
                    target = target[:-3]
                command_module = target.replace(path, root_package).replace(os.sep, ".")
                logger.info("scan command: %s", command_module)
                import_module(command_module)
        return self.collect()

MANAGER = CommandManager()


class CommandFromFunction(object):
    _ParserCreator = ParserCreator
    _manager = MANAGER

    def __init__(self, fn, argspec, help_dict=None, description=None):
        self.fn = fn
        self.parser_creator = self._ParserCreator(argspec, help_dict, description)
        self._manager.mark(self)

    def activate(self, level=1):
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name == "__main__":
            return self.run_as_command(sys.argv[1:])
        else:
            return self

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    @property
    def name(self):
        return text_(self.parser.prog)

    @reify
    def short_description(self):
        doc = getattr(self.fn, "__doc__", None)
        if doc is None:
            return ""
        return text_(doc.lstrip().split("\n")[0])

    @reify
    def parser(self):
        prog = self.fn.__module__
        if prog == "__main__":
            prog = None
        return self.parser_creator(prog=prog)

    def print_help(self, out=sys.stdout):
        self.parser.print_help(out)

    def run_as_command(self, args):
        try:
            parsed = self.parser.parse_args(args)
            args = [getattr(parsed, name) for name in self.parser.positionals]
            kwargs = {name: getattr(parsed, name) for name in self.parser.optionals}
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


def as_command(fn):
    argspec = inspect.getargspec(fn)
    doc = fn.__doc__ or ""
    help_dict = get_help_dict(doc)
    description = get_description(doc)
    return CommandFromFunction(fn, argspec, help_dict, description).activate(level=2)


# alias
handofcats = as_command


def describe(usage="command:\n", out=sys.stdout, package=None, name=None, level=1, scan=MANAGER.scan):
    if name is None:
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        package = frame.f_globals["__package__"]

    def write(msg):
        out.write(bytes_(text_(msg)))

    if name == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--full", default=False, action="store_true", dest="full_description")
        args = parser.parse_args(sys.argv[1:])
        commands = list(sorted(scan(package), key=lambda x: x.name))

        write("avaiable commands are here. (with --full option, showing full text)\n\n")
        for command in commands:
            if command.short_description:
                write(u"- {} -- {}\n".format(command.name, command.short_description))
            else:
                write(u"- {}\n".format(command.name))

        if args.full_description and commands:
            write(u"\n")
            for command in commands:
                write(u"\n---{}-------------------------------------\n".format(command.name))
                command.print_help(out)
