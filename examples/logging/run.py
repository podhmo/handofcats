from handofcats import as_command
import logging

logger = logging.getLogger(__name__)


@as_command
def run(ok: bool):
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
