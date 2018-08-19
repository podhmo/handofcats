import inspect
from logging import getLogger as get_logger
from .util import reify
logger = get_logger(__name__)


def option_name(name):
    return name.strip("_").replace("_", "-")


class Driver:
    def __init__(self, fn):
        self.fn = fn

    @reify
    def parser_factory(self):
        from .parsers import commandline
        return commandline.create_parser

    def run(self):
        fn = self.fn
        parser = self.parser_factory(fn, description=fn.__doc__)
        argspec = inspect.getfullargspec(fn)
        for k in argspec.kwonlyargs:
            parser.add_argument(f'{"-" if len(k) <= 1 else "--"}{option_name(k)}', required=True)
        args = parser.parse_args()
        params = vars(args).copy()
        return fn(**params)
