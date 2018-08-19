import re
import inspect
import logging
import sys
from handofcats.parsercreator import ArgumentParserCreator
from handofcats.commandcreator import CommandFromFunction
logger = logging.getLogger(__name__)


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


def as_command(fn=None, argv=None, level=2):
    def call(fn, level=1, argv=argv):
        if isinstance(fn, CommandFromFunction):
            cmd_creator = fn
        else:
            argspec = inspect.getargspec(fn)
            doc = fn.__doc__ or ""
            help_dict = get_help_dict(doc)
            description = get_description(doc)

            parser_creator = ArgumentParserCreator(argspec, help_dict, description)

            cmd_creator = CommandFromFunction(
                fn,
                parser_creator=parser_creator,
            )

        # dispatching from caller module
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name == "__main__":
            return cmd_creator.run_as_command(argv)
        else:
            return cmd_creator

    if fn is None:
        return call
    else:
        return call(fn, level=level, argv=argv)


# alias
handofcats = as_command
