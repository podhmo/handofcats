import typing as t
import dataclasses
from .injector import Injector
from .types import (
    TargetFunction,
    ArgumentParser,
    CustomizeSetupFunction,
    CustomizeActivateFunction,
    PrestringModule,
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
        self,
        argv=None,
    ):
        import argparse

        fn = self.fn
        config = self.config

        if self.config.ignore_expose:
            rest_argv = argv
        else:
            first_parser = argparse.ArgumentParser(add_help=False)
            customize.first_parser_setup(first_parser)

            fargs, rest_argv = first_parser.parse_known_args(argv)

            # code generation is needed
            if fargs.expose:
                from .actions import codegen

                factory = config.codegen_config.__class__
                if fargs.simple:
                    factory = config.codegen_config.as_simple
                config = dataclasses.replace(
                    config, codegen_config=factory(inplace=fargs.inplace)
                )

                return codegen.run_as_single_command(
                    self.setup_parser,
                    fn=fn,
                    argv=rest_argv,
                    config=config,
                )

        # run command normally
        from .actions import commandline

        return commandline.run_as_single_command(
            self.setup_parser, fn=fn, argv=rest_argv, config=config
        )

    def setup_parser(
        self,
        fn: t.Optional[TargetFunction] = None,
        *,
        config: t.Optional[Config] = None,
        m: t.Optional[PrestringModule] = None,
        customizations: t.Optional[t.List[CustomizeSetupFunction]] = None,
    ) -> t.Tuple[ArgumentParser, t.List[CustomizeActivateFunction]]:
        if fn is None:
            fn = self.fn
        if config is None:
            config = self.config
        if m is None:
            from .actions.commandline import _FakeModule

            m = _FakeModule()
        use_primitive_parser = config.codegen_config.use_primitive_parser

        # import argparse
        argparse = m.import_("argparse")
        m.sep()

        # parser = argparse.ArgumentParser(prog=fn.__name, help=fn.__doc__)
        if use_primitive_parser:
            parser = m.let("parser", argparse.ArgumentParser())
        else:
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

        if not use_primitive_parser:
            # parser.print_usage = parser.print_help  # type: ignore
            m.setattr(parser, "print_usage", parser.print_help)
            m.unnewline()
            m.stmt("  # type: ignore")

        injector = self.injector_class(fn)
        injector.inject(
            parser,
            callback=m.stmt,
            ignore_arguments=config.ignore_arguments,
            ignore_flags=config.ignore_flags,
        )

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
        # O(N), but do not mind.
        if fn in self.functions:
            return fn

        self.functions.append(fn)
        return fn

    __call__ = register

    def run(
        self,
        argv=None,
    ):
        import argparse

        functions = self.functions
        config = self.config

        if config.ignore_expose:
            rest_argv = argv
        else:
            first_parser = argparse.ArgumentParser(add_help=False)
            customize.first_parser_setup(first_parser)

            fargs, rest_argv = first_parser.parse_known_args(argv)

            if fargs.expose:
                # code generation is needed
                from .actions import codegen

                factory = config.codegen_config.__class__
                if fargs.simple:
                    factory = config.codegen_config.as_simple
                config = dataclasses.replace(
                    config, codegen_config=factory(inplace=fargs.inplace)
                )
                return codegen.run_as_multi_command(
                    self.setup_parser,
                    functions=functions,
                    argv=rest_argv,
                    config=config,
                )

        # run command normally
        from .actions import commandline

        return commandline.run_as_multi_command(
            self.setup_parser,
            functions=functions,
            argv=rest_argv,
            config=config,
        )

    def setup_parser(
        self,
        functions: t.Optional[t.List[TargetFunction]] = None,
        *,
        m: t.Optional[PrestringModule] = None,
        config: t.Optional[Config] = None,
        customizations: t.Optional[t.List[CustomizeSetupFunction]] = None,
    ) -> t.Tuple[ArgumentParser, t.List[CustomizeActivateFunction]]:
        if functions is None:
            functions = self.functions
        if config is None:
            config = self.config
        if m is None:
            from .actions.commandline import _FakeModule

            m = _FakeModule()

        # import argparse
        argparse = m.import_("argparse")
        m.sep()

        # parser = argparse.ArgumentParser()
        if config.codegen_config.use_primitive_parser:
            parser = m.let("parser", argparse.ArgumentParser())
        else:
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
            # parser.print_usage = parser.print_help  # type: ignore
            m.setattr(parser, "print_usage", parser.print_help)
            m.unnewline()
            m.stmt("  # type: ignore")

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

        for i, target_fn in enumerate(functions):
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

            if not config.codegen_config.use_primitive_parser:
                # sub_parser.print_usage = sub_parser.print_help  # type: ignore
                m.setattr(sub_parser, "print_usage", sub_parser.print_help)
                m.unnewline()
                m.stmt("  # type: ignore")

            Injector(target_fn).inject(
                sub_parser,
                callback=m.stmt,
                ignore_arguments=config.ignore_arguments,
                ignore_flags=config.ignore_flags,
            )

            # sub_parser.set_defaults(subcommand=fn)
            m.stmt(sub_parser.set_defaults(subcommand=fn))
            m.sep()
        return parser, activate_functions
