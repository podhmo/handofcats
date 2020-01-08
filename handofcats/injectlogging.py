import logging
import os
import sys


def setup(parser):
    logging_levels = list(logging._nameToLevel.keys())
    parser.add_argument(
        "--logging", choices=logging_levels, default=None
    )


def activate(params, *, logging_level=None, logging_format=None, logging_stream=None):
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
