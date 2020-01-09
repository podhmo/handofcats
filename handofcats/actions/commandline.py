import typing as t
import argparse
from . import TargetFunction, ContFunction, ArgumentParser


def setup(
    fn: TargetFunction, *, prog: t.Optional[str], description: t.Optional[str] = None
) -> (ArgumentParser, ContFunction):
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.print_usage = parser.print_help
    return parser, fn
