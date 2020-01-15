import logging
import os
import sys
from functools import partial


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
    m.stmt("# setup")
    logging_levels = list(logging._nameToLevel.keys())
    parser.add_argument("--logging", choices=logging_levels, default=None)
    return partial(logging_activate, m)


@codegen
def logging_activate(
    m, params, *, logging_level=None, logging_format=None, logging_stream=None
):
    logging_format = (
        logging_format
        or "level:%(levelname)s	name:%(name)s	where:%(filename)s:%(lineno)s	relative:%(relativeCreated)s	message:%(message)s"
    )

    if os.environ.get("DEBUG"):
        logging_level = logging.DEBUG
        print("** {where}: DEBUG=1, activate logging **".format(where=__name__))

    if os.environ.get("LOGGING_LEVEL"):
        logging_level = logging._nameToLevel.get(os.environ["LOGGING_LEVEL"])
    if os.environ.get("LOGGING_FORMAT"):
        logging_format = os.environ["LOGGING_FORMAT"]
    if os.environ.get("LOGGING_STREAM"):
        logging_stream = getattr(sys, os.environ["LOGGING_STREAM"])

    if "logging" in params:
        level = params.pop("logging", None)
        if level is not None:
            logging_level = level

    if logging_level is not None:
        logging.basicConfig(
            level=logging_level, format=logging_format, stream=logging_stream,
        )
