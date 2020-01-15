import typing as t

import logging

logger = logging.getLogger(__name__)
def run(ok: bool):
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('ok', action='store_true', help='-')

    # setup logging
    import logging
    logging_level_choices = list(logging._nameToLevel.keys())
    parser.add_argument('--logging', choices=logging_level_choices, default=None)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    import os
    import sys

    # activate logging
    logging_format = None or 'level:%(levelname)s\tname:%(name)s\twhere:%(filename)s:%(lineno)s\trelative:%(relativeCreated)s\tmessage:%(message)s'
    if os.environ.get('DEBUG'):
        logging_level = logging.DEBUG
        print('** {where}: DEBUG=1, activate logging **'.format(where=__name__), file=sys.stderr)
    if os.environ.get('LOGGING_LEVEL'):
        logging_level = logging._nameToLevel.get(os.environ['LOGGING_LEVEL'])
    if os.environ.get('LOGGING_FORMAT'):
        logging_format = os.environ['LOGGING_FORMAT']
    if os.environ.get('LOGGING_STREAM'):
        logging_stream = getattr(sys, os.environ['LOGGING_STREAM'])
    if 'logging' in params:
        level = params.pop('logging', None)
        if level is not None:
            logging_level = level
    if logging_level is not None:
        logging.basicConfig(level=logging_level, format=logging_format, stream=logging_stream)

    return run(**params)


if __name__ == '__main__':
    main()
