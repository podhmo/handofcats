import logging
import os
import sys
from functools import partial


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
        "--simple", action="store_true", help="use minimum expression",
    )  # xxx (./actions/codegen.py)
    return first_parser_activate


def first_parser_activate(params):
    params.pop("expose", None)  # xxx: ./actions/codegen.py
    params.pop("inplace", None)  # xxx: ./actions/codegen.py
    params.pop("simple", None)  # xxx: ./actions/codegen.py


def logging_setup(parser, *, debug: bool = False):
    logging_levels = list(logging._nameToLevel.keys())
    parser.add_argument("--logging", choices=logging_levels, default=None)
    return partial(logging_activate, debug=debug)


def logging_activate(
    params,
    *,
    debug: bool = False,
    logging_level=None,
    logging_format=None,
    logging_stream=None,
    logging_time=None,  # "relative", "asctime", None
):
    time_format_map = {
        "relative": "relative:%(relativeCreated)s	",
        "asctime": "asctime:%(asctime)s	",
        None: "",
    }
    if os.environ.get("LOGGING_TIME"):
        logging_time = os.environ["LOGGING_TIME"]

    logging_format = (
        logging_format
        or f"level:%(levelname)s	name:%(name)sL%(lineno)s	{time_format_map.get(logging_time, '')}message:%(message)s"
    )

    if debug or bool(os.environ.get("DEBUG", "").strip()):
        logging_level = logging.DEBUG
        print(
            "** {where}: DEBUG=1, activate logging **".format(where=__name__),
            file=sys.stderr,
        )

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
