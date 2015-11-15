# -*- coding:utf-8 -*-
import argparse
import sys
from handofcats import as_command
try:
    from importlib import import_module, machinery
except ImportError:
    from importlib2 import import_module, machinery


def import_symbol(module, name):
    module = import_module(module)
    return getattr(module, name)


def import_symbol_from_filepath(path, name, module_id=None):
    module_id = module_id or path.replace("/", "_").rstrip(".py")
    module = machinery.SourceFileLoader(module_id, path).load_module()
    return getattr(module, name)


def module_symbol(path):
    try:
        module, name = path.rsplit(":", 1)
        return import_symbol(module, name)
    except ValueError:
        raise argparse.ArgumentTypeError("must be in 'module:attrs' format")
    except ImportError:
        sys.path.append(".")
        return import_symbol_from_filepath(module, name)


def main():
    parser = argparse.ArgumentParser()
    help_text = "target EntryPoint. (must be in 'module:attrs' format)"
    parser.add_argument("entry_point", type=module_symbol, help=help_text)

    args, rest_argv = parser.parse_known_args(sys.argv[1:])
    as_command(args.entry_point, argv=rest_argv, level=3)
