# -*- coding:utf-8 -*-
import argparse
import sys
from handofcats import as_command
from importlib import import_module


def import_symbol(module, name):
    module = import_module(module)
    return getattr(module, name)


def import_symbol_from_filepath(path, name, module_id=None):
    try:
        from importlib import machinery
    except ImportError:
        # patching for import machinery
        # https://bitbucket.org/ericsnowcurrently/importlib2/issues/8/unable-to-import-importlib2machinery
        import importlib2._fixers as f
        fix_importlib_original = f.fix_importlib

        def fix_importlib(ns):
            if ns["__name__"] == 'importlib2.machinery':
                class _LoaderBasics:
                    load_module = object()
                ns["_LoaderBasics"] = _LoaderBasics

                class FileLoader:
                    load_module = object()
                ns["FileLoader"] = FileLoader

                class _NamespaceLoader:
                    load_module = object()
                    module_repr = object()
                ns["_NamespaceLoader"] = _NamespaceLoader
            fix_importlib_original(ns)
        f.fix_importlib = fix_importlib
        from importlib2 import machinery

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
