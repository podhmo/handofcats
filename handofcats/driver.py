import itertools
from logging import getLogger as get_logger
from .util import reify
logger = get_logger(__name__)


class Driver:
    def __init__(self, fn):
        self.fn = fn

    @reify
    def accessor(self):
        from .accessor import Accessor
        return Accessor(self.fn)

    def create_parser(self, fn, *, argv=None, description=None):
        if "--expose" in (argv or []):
            from .parsers import expose
            parser = expose.create_parser(fn, description=description or fn.__doc__)
        else:
            from .parsers import commandline
            parser = commandline.create_parser(fn, description=description or fn.__doc__)
            parser.add_argument("--expose", action="store_true")  # xxx (for ./expose.py)
        return parser

    def setup_parser(self, parser):
        arguments = [(opt, None) for opt in self.accessor.arguments]
        flags = [(opt, opt.required) for opt in self.accessor.flags]

        for opt, required in itertools.chain(arguments, flags):
            kwargs = {}
            if required is not None:
                kwargs["required"] = required
            if opt.default is not None:
                kwargs["default"] = opt.default
            if opt.type and opt.type != str:
                if opt.type != bool:
                    kwargs["type"] = opt.type
                else:
                    action = "store_true"
                    if opt.default is True:
                        action = "store_false"
                    kwargs.pop("required", None)
                    kwargs.pop("default", None)
                    kwargs["action"] = action

            logger.debug("add_argument %s %r", opt.option_name, kwargs)
            parser.add_argument(opt.option_name, **kwargs)

    def run(self, argv=None):
        fn = self.fn
        parser = self.create_parser(fn, argv=argv, description=fn.__doc__)
        self.setup_parser(parser)
        args = parser.parse_args(argv)
        params = vars(args).copy()
        params.pop("expose", None)  # xxx: for ./parsers/expose.py
        return fn(**params)
