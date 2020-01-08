import logging

logger = logging.getLogger(__name__)


def run(ok: bool):
    logger.debug(""""debug" logger's message""")
    logger.info(""""info" logger's message""")
    logger.warning(""""warning" logger's message""")
    logger.error(""""error" logger's message""")
    logger.critical(""""critical" logger's message""")

    logger.info("""
MULTILINE MESSAGE

- hello
- byebye
""")
