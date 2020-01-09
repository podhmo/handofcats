import functools
from ._callback import CallbackArgumentParser


class ParseArgsCalled(Exception):
    def __init__(self, *, fn, history):
        self.fn = fn
        self.history = history


def on_parse_args(*, fn, history):
    raise ParseArgsCalled(fn=fn, history=history)


create_parser = functools.partial(CallbackArgumentParser, on_parse_args)
