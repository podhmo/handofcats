from functools import partial
import contextlib
from .actions._fake import Fail

block = partial(contextlib.suppress, Fail)


class _Marker:
    def __init__(self, name: str) -> None:
        self.name = name

    def __call__(self, fn):
        setattr(fn, self.name, True)
        return fn

    def is_(self, fn):
        return getattr(fn, self.name, False)


codegen = _Marker("_codegen_need")
need_codegen = codegen.is_


def first_parser_setup(parser):
    parser.add_argument(
        "--expose",
        action="store_true",
        help="dump generated code. with --inplace, eject from handofcats dependency",
    )  # xxx (./actions/codegen.py)
    parser.add_argument(
        "--inplace", action="store_true", help="overwrite file"
    )  # xxx (./actions/codegen.py)
    parser.add_argument(
        "--untyped", action="store_true", help="untyped expression is dumped",
    )  # xxx (./actions/codegen.py)
    return first_parser_activate


def first_parser_activate(params):
    params.pop("expose", None)  # xxx: ./actions/codegen.py
    params.pop("inplace", None)  # xxx: ./actions/codegen.py
    params.pop("untyped", None)  # xxx: ./actions/codegen.py


@codegen
def logging_setup(m, parser):
    list_ = m.symbol(list)

    m.sep()
    m.stmt("# setup logging")
    logging_ = m.import_("logging")

    # logging_level_choices = list(logging._nameToLevel.keys())
    logging_level_choices = m.let(
        "logging_level_choices", list_(logging_._nameToLevel.keys())
    )

    # parser.add_argument("--logging", choices=logging_level_choices, default=None)
    m.stmt(
        parser.add_argument("--logging", choices=logging_level_choices, default=None)
    )
    m.sep()

    return partial(logging_activate, m)


DEFAULT_LOGGING_FORMAT = "level:%(levelname)s	name:%(name)s	where:%(filename)s:%(lineno)s	relative:%(relativeCreated)s	message:%(message)s"


@codegen
def logging_activate(
    m, params, *, logging_level=None, logging_format=None, logging_stream=None
):
    os_ = m.import_("os")
    sys_ = m.import_("sys")
    logging_ = m.import_("logging")
    print_ = m.symbol(print)
    getattr_ = m.symbol(getattr)

    m.sep()
    m.stmt("# activate logging")

    # logging_level = m.let("logging_level", None)

    # logging_format = logging_format or DEFAULT_LOGGING_FORMAT
    # BUG: None or DEFAULT_LOGGING_FORMAT
    logging_format = m.let(
        "logging_format",
        m.or_(m.symbol(logging_format), m.constant(DEFAULT_LOGGING_FORMAT)),
    )

    # if os.environ.get("DEBUG"):
    with block():
        with m.if_(os_.environ.get("DEBUG")):
            # logging_level = logging.DEBUG
            logging_level = m.let("logging_level", logging_.DEBUG)

            # print("** {where}: DEBUG=1, activate logging **".format(where=__name__))
            m.stmt(
                print_(
                    m.format_(
                        "** {where}: DEBUG=1, activate logging **",
                        where="__name__",
                    ),
                    file=sys_.stderr,
                )
            )

    # if os.environ.get("LOGGING_LEVEL"):
    with block():
        with m.if_(os_.environ.get("LOGGING_LEVEL")):

            # logging_level = logging._nameToLevel.get(os.environ["LOGGING_LEVEL"])
            logging_level = m.let(
                "logging_level",
                logging_._nameToLevel.get(os_.environ["LOGGING_LEVEL"]),
            )

    # if os.environ.get("LOGGING_FORMAT"):
    with block():
        with m.if_(os_.environ.get("LOGGING_FORMAT")):

            # logging_format = os.environ["LOGGING_FORMAT"]
            logging_format = m.let("logging_format", os_.environ["LOGGING_FORMAT"],)

    # if os.environ.get("LOGGING_STREAM"):
    with block():
        with m.if_(os_.environ.get("LOGGING_STREAM")):
            # logging_stream = getattr(sys, os.environ["LOGGING_STREAM"])
            logging_stream = m.let(
                "logging_stream", getattr_(sys_, os_.environ["LOGGING_STREAM"])
            )

    # if "logging" in params:
    with block():
        with m.if_(m.in_(m.constant("logging"), params)):

            # level = params.pop("logging", None)
            level = m.let("level", params.pop("logging", None))

            # if level is not None:
            with block():
                with m.if_(m.is_not(level, None)):

                    # logging_level = level

                    logging_level = m.let("logging_level", level)

    # if logging_level is not None:
    with block():
        with m.if_(m.is_not(logging_level, None)):

            # logging.basicConfig(
            #     level=logging_level, format=logging_format, stream=logging_stream,
            # )
            m.stmt(
                logging_.basicConfig(
                    level=logging_level, format=logging_format, stream=logging_stream,
                )
            )
    m.sep()
