import logging

logger = logging.getLogger(__name__)


def run(ok: bool):
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
