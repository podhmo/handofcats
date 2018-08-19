import argparse
from logging import getLogger as get_logger
from . import as_command
from . import util
logger = get_logger(__name__)


def import_symbol(path, sep=":", logger=logger):
    try:
        return util.import_symbol(path, sep=sep, logger=logger)
    except ValueError as e:
        logger.info(str(e), exc_info=True)
        import argparse  # xxx
        raise argparse.ArgumentTypeError("must be in 'module:attrs' format")


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    help_text = "target EntryPoint. (must be in 'module:attrs' format)"
    parser.add_argument("entry_point", type=import_symbol, help=help_text)

    args, rest_argv = parser.parse_known_args(argv)
    as_command(args.entry_point, argv=rest_argv, level=3)


if __name__ == "__main__":
    main()
