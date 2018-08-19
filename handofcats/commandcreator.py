# -*- coding:utf-8 -*-
import sys
import logging
from cached_property import cached_property as reify
from .compat import text_
logger = logging.getLogger(__name__)


class CommandFromFunction(object):
    def __init__(self, fn, parser_creator):
        self.fn = fn
        self.parser_creator = parser_creator

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

    def run_as_command(self, args=None):
        try:
            parsed = self.parser.parse_args(args)
            args = [getattr(parsed, name) for name in self.parser.positionals]
            kwargs = {name: getattr(parsed, name) for name in self.parser.optionals}
        except Exception as e:
            sys.stderr.write("{!r}\n".format(e))
            logger.warning("error is occured", exc_info=True)
            sys.exit(-1)
        self.fn(*args, **kwargs)
