import logging

# from: https://docs.python.org/3/howto/logging.html


def use_root_logger():
    logging.debug("This message should go to the log file")
    logging.info("So should this")
    logging.warning("And this, too")
