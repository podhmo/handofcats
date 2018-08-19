import argparse


def create_parser(fn, description=None):
    parser = argparse.ArgumentParser(description=fn.__doc__)
    parser.print_usage = parser.print_help
    return parser
