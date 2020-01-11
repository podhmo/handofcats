import typing as t
from .injector import Injector
from .types import (
    TargetFunction,
    ArgumentParser,
    CustomizeSetupFunction,
    CustomizeActivateFunction,
)
from . import customize
from prestring.naming import titleize


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
        if fargs.expose:  # "--expose" ?
            from .actions import codegen

            return codegen.run_as_single_command(
                fn, rest, inplace=fargs.inplace, typed=fargs.typed,
            )
        else:
            from .actions import commandline

            return commandline.run_as_single_command(
                self.setup_parser, fn, rest, ignore_logging=self.ignore_logging
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

    def run(
        self, argv=None,
    ):
        import argparse

        first_parser = argparse.ArgumentParser(add_help=False)
        customize.first_parser_setup(first_parser)

        fargs, rest = first_parser.parse_known_args(argv)
        functions = self.functions
        if fargs.expose:  # "--expose" ?
            return self._run_expose_action(
                functions, rest, inplace=fargs.inplace, typed=fargs.typed
            )
        else:
            return self._run_command_line(rest)

    def _run_command_line(
        self, functions: t.List[TargetFunction], argv: t.Optional[str] = None
    ) -> t.Any:
        from .actions import commandline

        m = commandline.setup_module()

        customizations = []
        if not self.ignore_logging:
            # TODO: include generated code, emitted by `--expose`
            customizations.append(customize.logging_setup)

        parser, activate_functions = self.setup_parser(
            m, self.functions, customizations=customizations
        )
        args = parser.parse_args(argv)
        params = vars(args).copy()

        for activate in activate_functions:
            activate(params)

        subcommand = params.pop("subcommand")
        return subcommand(**params)

    def _run_expose_action(
        self,
        functions: t.List[TargetFunction],
        argv: t.Optional[str] = None,
        *,
        outname: str = "main",
        inplace: bool = False,
        typed: bool = False,
    ) -> t.Any:
        """ generate main() code

        something like

        ```
        ```
        """

        from .actions import codegen

        m = codegen.setup_module()
        if outname in [fn.__name__ for fn in self.functions]:
            outname = titleize(outname)  # main -> Main

        if typed:
            m.sep()
            m.from_("typing").import_("Optional, List  # noqa: E402")
            m.sep()
            mdef = m.def_(
                outname, "argv: Optional[List[str]] = None", return_type="None"
            )
        else:
            mdef = m.def_(outname, "argv=None")

        # def main(argv=None):
        with mdef:
            parser, _ = self.setup_parser(m, fn, customizations=[])

            # args = parser.parse_args(argv)
            args = m.let("args", parser.parse_args(m.symbol("argv")))

            # params = vars(args).copy()
            params = m.let("params", m.symbol("vars")(args).copy())

            # subcommand = params.pop("subcommand")
            m.let("subcommand", params.pop("subcommand"))

            # return subcommand(**params)
            m.return_(f"subcommand(**params)")

        # if __name__ == "__main__":
        with m.if_("__name__ == '__main__'"):
            # main()
            m.stmt(f"{outname}()")

        fake = functions[0]
        codegen.emit(m, fake, inplace=inplace)

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
