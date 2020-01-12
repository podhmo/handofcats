import typing as t
from .injector import Injector
from .types import (
    TargetFunction,
    ArgumentParser,
    CustomizeSetupFunction,
    CustomizeActivateFunction,
)
from .config import Config, default_config
from . import customize


class Driver:
    injector_class = Injector

    def __init__(self, fn: TargetFunction, *, config: Config = default_config):
        self.fn = fn
        self.config = config

    def register(self, fn: TargetFunction) -> TargetFunction:
        self.fn = fn  # overwrite
        return fn

    __call__ = register

    def run(
        self, argv=None,
    ):
        import argparse

        fn = self.fn

        if self.config.ignore_expose:
            rest_argv = argv
        else:
            first_parser = argparse.ArgumentParser(add_help=False)
            customize.first_parser_setup(first_parser)

            fargs, rest_argv = first_parser.parse_known_args(argv)

            # code generation is needed
            if fargs.expose:
                from .actions import codegen

                return codegen.run_as_single_command(
                    self.setup_parser,
                    fn=fn,
                    argv=rest_argv,
                    inplace=fargs.inplace,
                    typed=not fargs.untyped,
                )

        # run command normally
        from .actions import commandline

        return commandline.run_as_single_command(
            self.setup_parser, fn=fn, argv=rest_argv, config=self.config
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
                formatter_class=m.symbol(type)(
                    "_HelpFormatter",
                    (
                        argparse.ArgumentDefaultsHelpFormatter,
                        argparse.RawTextHelpFormatter,
                    ),
                    {},
                ),
            ),
        )

        # parser.print_usage = parser.print_help  # type: ignore
        m.setattr(parser, "print_usage", parser.print_help)
        m.unnewline()
        m.stmt("  # type: ignore")

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

    def __init__(
        self,
        functions: t.List[TargetFunction] = None,
        *,
        config: Config = default_config,
    ):
        self.config = config
        self.functions: t.List[TargetFunction] = functions or []

    def register(self, fn: TargetFunction) -> TargetFunction:
        self.functions.append(fn)
        return fn

    __call__ = register

    def run(
        self, argv=None,
    ):
        import argparse

        functions = self.functions

        if self.config.ignore_expose:
            rest_argv = argv
        else:
            first_parser = argparse.ArgumentParser(add_help=False)
            customize.first_parser_setup(first_parser)

            fargs, rest_argv = first_parser.parse_known_args(argv)

            if fargs.expose:
                # code generation is needed
                from .actions import codegen

                return codegen.run_as_multi_command(
                    self.setup_parser,
                    functions=functions,
                    argv=rest_argv,
                    inplace=fargs.inplace,
                    typed=not fargs.untyped,
                )

        # run command normally
        from .actions import commandline

        return commandline.run_as_multi_command(
            self.setup_parser, functions=functions, argv=rest_argv, config=self.config,
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
        parser = m.let(
            "parser",
            argparse.ArgumentParser(
                formatter_class=m.symbol(type)(
                    "_HelpFormatter",
                    (
                        argparse.ArgumentDefaultsHelpFormatter,
                        argparse.RawTextHelpFormatter,
                    ),
                    {},
                ),
            ),
        )

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

        for i, target_fn in enumerate(self.functions):
            # fn = <target function>
            fn = m.let("fn", m.symbol(target_fn))
            if i > 0:
                m.unnewline()
                m.stmt("  # type: ignore")

            # sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
            sub_parser = m.let(
                "sub_parser",
                subparsers.add_parser(
                    m.getattr(fn, "__name__"),
                    help=m.getattr(fn, "__doc__"),
                    formatter_class=parser.formatter_class,
                ),
            )
            Injector(target_fn).inject(sub_parser, callback=m.stmt)

            # sub_parser.set_defaults(subcommand=fn)
            m.stmt(sub_parser.set_defaults(subcommand=fn))
            m.sep()
        return parser, activate_functions
