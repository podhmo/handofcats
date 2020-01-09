import typing as t
import argparse


def create_parser(*, prog: t.Optional[str], description: t.Optional[str] = None):
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.print_usage = parser.print_help
    return parser
