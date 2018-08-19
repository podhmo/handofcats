import argparse


def create_parser(fn, description=None):
    parser = argparse.ArgumentParser(description=description)
    parser.print_usage = parser.print_help
    return parser
