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

    def run(self, argv=None):
        fn = self.fn
        parser = self.parser_factory(fn, description=fn.__doc__)
        argspec = inspect.getfullargspec(fn)

        # TODO: type
        # TODO: default value
        # TODO: positional argument
        for k in argspec.kwonlyargs:
            if len(k) <= 1:
                option = f"-{option_name(k)}"
            else:
                option = f"--{option_name(k)}"

            typ = argspec.annotations.get(k)
            if typ is str:
                parser.add_argument(option, required=True)
            elif typ is int:
                parser.add_argument(option, required=True, type=int)
            elif typ is float:
                parser.add_argument(option, required=True, type=float)
            else:
                parser.add_argument(option, required=True)

        args = parser.parse_args(argv)
        params = vars(args).copy()
        return fn(**params)
