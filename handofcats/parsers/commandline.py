import argparse
import inspect
from logging import getLogger as get_logger
logger = get_logger(__name__)


def option_name(self, name):
    return name.strip("_").replace("_", "-")


def create_parser(fn, description=None):
    argspec = inspect.getfullargspec(fn)
    parser = argparse.ArgumentParser(description=fn.__doc__)
    parser.print_usage = parser.print_help

    for k in argspec.kwonlyargs:
        parser.add_argument(f'{"-" if len(k) <= 1 else "--"}{k.replace("_", "-")}', required=True)
    return parser
