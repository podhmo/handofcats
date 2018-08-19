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
                kwargs = {}
                if argspec.kwonlydefaults and argspec.kwonlydefaults.get(k):
                    kwargs["default"] = argspec.kwonlydefaults.get(k)
                parser.add_argument(option, **kwargs, required=True)
            elif typ is bool:
                kwargs = {"action": "store_true"}
                if argspec.kwonlydefaults and argspec.kwonlydefaults.get(k) is True:
                    kwargs["action"] = "store_false"
                parser.add_argument(option, **kwargs)
            elif typ in (int, float):
                kwargs = {"type": typ}
                if argspec.kwonlydefaults and argspec.kwonlydefaults.get(k):
                    kwargs["default"] = argspec.kwonlydefaults.get(k)
                parser.add_argument(option, **kwargs, required=True)
            else:
                kwargs = {}
                if argspec.kwonlydefaults and argspec.kwonlydefaults.get(k):
                    kwargs["default"] = argspec.kwonlydefaults.get(k)
                parser.add_argument(option, **kwargs, required=True)

        args = parser.parse_args(argv)
        params = vars(args).copy()
        return fn(**params)
