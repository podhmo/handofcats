import logging
import os


def setup(parser):
    logging_levels = list(logging._nameToLevel.keys())
    parser.add_argument(
        "--logging", choices=logging_levels, default="INFO", help="(default: INFO)"
    )


def activate(params, *, logging_level=None, logging_format=None):
    logging_format = (
        logging_format
        or "level:%(levelname)s	name:%(name)s	where:%(filename)s:%(lineno)s	message:%(message)s"
    )

    if os.environ.get("DEBUG"):
        logging_level = logging.DEBUG
    if os.environ.get("LOGGING_LEVEL"):
        logging_level = logging._nameToLevel.get(os.environ["LOGGING_LEVEL"])

    if "logging" in params:
        level = params.pop("logging", None)
        if level is not None:
            logging_level = level

    if os.environ.get("LOGGING_LEVEL"):
        logging_level = logging._nameToLevel.get(os.environ["LOGGING_LEVEL"])
    if os.environ.get("LOGGING_FORMAT"):
        logging_format = logging._nameToFormat.get(os.environ["LOGGING_FORMAT"])

    if logging_level is not None:
        logging.basicConfig(level=logging_level, format=logging_format)
