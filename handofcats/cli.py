# -*- coding:utf-8 -*-
import argparse
import sys
from handofcats import as_command
from importlib import import_module


def import_symbol(path):
    module, name = path.rsplit(":", 1)
    module = import_module(module)
    return getattr(module, name)


def module_symbol(path):
    try:
        module, name = path.rsplit(":", 1)
        return path
    except ValueError:
        raise argparse.ArgumentTypeError("must be in 'module:attrs' format")


def main():
    parser = argparse.ArgumentParser()
    help_text = "target EntryPoint. (must be in 'module:attrs' format)"
    parser.add_argument("entry_point", type=module_symbol, help=help_text)

    args, rest_argv = parser.parse_known_args(sys.argv[1:])
    entry_point = import_symbol(args.entry_point)
    as_command(entry_point, argv=rest_argv, level=3)
