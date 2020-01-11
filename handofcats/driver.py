import typing as t
from .injector import Injector
from .types import (
    TargetFunction,
    ArgumentParser,
    CustomizeSetupFunction,
    CustomizeActivateFunction,
)
from . import customize


class Driver:
    injector_class = Injector

    def __init__(self, *, ignore_logging=False):
        self.ignore_logging = ignore_logging

    def run(
        self, fn: TargetFunction, argv=None,
    ):
        import argparse

        first_parser = argparse.ArgumentParser(add_help=False)
        customize.first_parser_setup(first_parser)

        fargs, rest = first_parser.parse_known_args(argv)

        # run command normally
        if not fargs.expose:
            from .actions import commandline

            return commandline.run_as_single_command(
                self.setup_parser, fn=fn, argv=rest, ignore_logging=self.ignore_logging
            )

        # code generation is needed
        from .actions import codegen

        return codegen.run_as_single_command(
            self.setup_parser,
            fn=fn,
            argv=rest,
            inplace=fargs.inplace,
            typed=fargs.typed,
        )

    def setup_parser(
        self,
        m,
        fn: TargetFunction,
        argv=None,
        *,
        customizations: t.Optional[t.List[CustomizeSetupFunction]] = None,
    ) -> t.Tuple[ArgumentParser, t.List[CustomizeActivateFunction]]:
        # import argparse
        argparse = m.import_("argparse")
        m.sep()

        # parser = argparse.ArgumentParser(prog=fn.__name, help=fn.__doc__)
        parser = m.let(
            "parser",
            argparse.ArgumentParser(
                prog=m.getattr(m.symbol(fn), "__name__"),
                description=m.getattr(m.symbol(fn), "__doc__"),
            ),
        )

        # parser.print_usage = parser.print_help
        m.setattr(parser, "print_usage", parser.print_help)

        injector = self.injector_class(fn)
        injector.inject(parser, callback=m.stmt)

        activate_functions = []
        for setup in customizations or []:
            afn = setup(parser)
            if afn is not None:
                activate_functions.append(afn)
        return parser, activate_functions


class MultiDriver:
    injector_class = Injector

    def __init__(self, *, ignore_logging=False):
        self.ignore_logging = ignore_logging
        self.functions: t.List[TargetFunction] = []

    def register(self, fn: TargetFunction) -> None:
        self.functions.append(fn)

    __call__ = register

    def run(
        self, argv=None,
    ):
        import argparse

        first_parser = argparse.ArgumentParser(add_help=False)
        customize.first_parser_setup(first_parser)

        fargs, rest = first_parser.parse_known_args(argv)
        functions = self.functions

        # run command normally
        if not fargs.expose:
            from .actions import commandline

            return commandline.run_as_multi_command(
                self.setup_parser,
                functions=functions,
                argv=rest,
                ignore_logging=self.ignore_logging,
            )

        # code generation is needed
        from .actions import codegen

        return codegen.run_as_multi_command(
            self.setup_parser,
            functions=functions,
            argv=rest,
            inplace=fargs.inplace,
            typed=fargs.typed,
        )

    def setup_parser(
        self,
        m,
        functions: t.List[TargetFunction],
        *,
        customizations: t.Optional[t.List[CustomizeSetupFunction]] = None,
    ) -> t.Tuple[ArgumentParser, t.List[CustomizeActivateFunction]]:
        # import argparse
        argparse = m.import_("argparse")
        m.sep()

        # parser = argparse.ArgumentParser()
        parser = m.let("parser", argparse.ArgumentParser(),)

        activate_functions = []
        for setup in customizations or []:
            afn = setup(parser)
            if afn is not None:
                activate_functions.append(afn)

        # subparesrs = parser.add_subparsers(title="subparesrs", dest="subcommand")
        subparsers = m.let(
            "subparsers", parser.add_subparsers(title="subcommands", dest="subcommand")
        )

        # subparsers.required = True
        m.setattr(subparsers, "required", True)  # for py3.6
        m.sep()

        for target_fn in self.functions:
            # fn = <target function>
            fn = m.let("fn", m.symbol(target_fn))

            # sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
            sub_parser = m.let(
                "sub_parser",
                subparsers.add_parser(
                    m.getattr(fn, "__name__"), help=m.getattr(fn, "__doc__")
                ),
            )
            Injector(target_fn).inject(sub_parser, callback=m.stmt)

            # sub_parser.set_defaults(subcommand=fn)
            m.stmt(sub_parser.set_defaults(subcommand=fn))
            m.sep()
        return parser, activate_functions
