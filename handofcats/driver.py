import typing as t
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

    def _setup_type(self, opt, kwargs):
        if opt.type == bool:
            action = "store_true"
            if opt.default is True:
                action = "store_false"
            kwargs.pop("required", None)
            kwargs.pop("default", None)
            kwargs["action"] = action
        elif opt.type in (int, float):
            kwargs["type"] = opt.type
        else:
            from collections.abc import Sequence
            if hasattr(opt.type, "__origin__") and hasattr(opt.type, "__args__"):
                try:
                    # for Optional
                    nonetype = type(None)
                    if opt.type.__origin__ == t.Union and nonetype in opt.type.__args__ and len(
                        opt.type.__args__
                    ) == 2:
                        item_type = opt._replace(
                            type=[t for t in opt.type.__args__ if t is not nonetype][0]
                        )
                        self._setup_type(item_type, kwargs)

                    # for sequence (e.g. t.List[int], t.Tuple[str])
                    elif issubclass(opt.type.__origin__, Sequence):
                        kwargs["action"] = "append"
                        item_type = opt._replace(type=opt.type.__args__[0])
                        self._setup_type(item_type, kwargs)
                except:
                    logger.info(
                        "unexpected generic type is found (type=%s)", opt.type, exc_info=True
                    )
            elif hasattr(opt.type, "__supertype__"):  # for NewType
                # choices support (tentative)
                if hasattr(opt.type, "choices"):
                    kwargs["choices"] = opt.type.choices
                origin_type = opt._replace(type=opt.type.__supertype__)
                self._setup_type(origin_type, kwargs)
            elif issubclass(opt.type, (list, tuple)):
                kwargs["action"] = "append"
            else:
                logger.info("unexpected type is found (type=%s)", opt.type)

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
                self._setup_type(opt, kwargs)
            if kwargs.get("action") == "append" and not opt.option_name.startswith("-"):
                kwargs["nargs"] = "*"
                kwargs.pop("action")

            if "default" in kwargs:
                kwargs["help"] = "(default: {!r})".format(kwargs["default"])

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
