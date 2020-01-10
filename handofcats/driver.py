import typing as t
import sys
from .injector import Injector
from .actions import TargetFunction, ContFunction, ArgumentParser
from . import customize
from prestring.naming import titleize


class Driver:
    injector_class = Injector

    def __init__(self, *, ignore_logging=False):
        self.ignore_logging = ignore_logging

    def run(
        self, fn: TargetFunction, argv=None,
    ):
        if "--expose" in (argv or []):
            return self._run_expose_action(fn, argv)
        else:
            return self._run_command_line(fn, argv)

    def _run_command_line(
        self, fn: TargetFunction, argv: t.Optional[str] = None
    ) -> t.Any:
        from .actions import commandline

        m = commandline.setup_module()

        customizations = []
        if not self.ignore_logging:
            # TODO: include generated code, emitted by `--expose`
            customizations.append(customize.logging_setup)

        parser, activate_functions = self.setup_parser(
            m, fn, customizations=customizations
        )
        args = parser.parse_args(argv)
        params = vars(args).copy()

        for activate in activate_functions:
            activate(params)
        return fn(**params)

    def _run_expose_action(
        self,
        fn: TargetFunction,
        argv: t.Optional[str] = None,
        *,
        outname: str = "main",
    ) -> None:
        """ generate main() code

        something like

        ```
        def main(argv=None):
            import argparse

            parser = argparse.ArgumentParser(prog=hello.__name__, description=hello.__doc__)
            parser.print_usage = parser.print_help

            # adding code, by self.setup_parser(). e.g.
            # parser.add_argument('--name', required=False, default='world', help="(default: 'world')")
            # parser.add_argument('--debug', action="store_true")

            args = parser.parse_args(argv)
            params = vars(args).copy()
            return hello(**params)

        if __name__ == "__main__":
            main()
        ```
        """
        from .actions import codegen

        # TODO: use first_parser
        inplace = "--inplace" in (argv or [])
        typed = "--typed" in (argv or [])

        m = codegen.setup_module()

        if fn.__name__ == outname:
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
            _ = m.let("params", m.symbol("vars")(args).copy())

            # return fn(**params)
            m.return_(f"{fn.__name__}(**params)")

        # if __name__ == "__main__":
        with m.if_("__name__ == '__main__'"):
            # main()
            m.stmt(f"{outname}()")

        codegen.emit(m, fn, inplace=inplace)

    def setup_parser(
        self,
        m,
        fn: TargetFunction,
        argv=None,
        *,
        customizations: t.Optional[t.List[customize.SetupFunction]] = None,
    ) -> t.Tuple[ArgumentParser, t.List[customize.ActivateFunction]]:
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
        if "--expose" in (argv or sys.argv[1:]):
            return self._run_expose_action(self.functions[0], argv)
        else:
            return self._run_command_line(self.functions[0], argv)

    def _run_command_line(
        self, fn: TargetFunction, argv: t.Optional[str] = None
    ) -> t.Any:
        from .actions import commandline

        m, parser, cont = commandline.setup_for_multi_command(fn)
        return self._run(
            m, parser, fn, argv, ignore_logging=self.ignore_logging, cont=cont
        )

    def _run_expose_action(
        self, fn: TargetFunction, argv: t.Optional[str] = None
    ) -> t.Any:
        from .actions import codegen

        inplace = "--inplace" in (argv or sys.argv[1:])
        typed = "--typed" in (argv or sys.argv[1:])

        m, parser, cont = codegen.setup_for_multi_command(
            fn, inplace=inplace, typed=typed
        )
        return self._run(m, parser, fn, argv, ignore_logging=True, cont=cont)

    def _run(
        self,
        m,
        parser,
        fn: TargetFunction,
        argv=None,
        *,
        ignore_logging=False,
        cont: t.Optional[ContFunction],
    ):
        # TODO: include generated code, emitted by `--expose`
        if not ignore_logging:
            customize.logging_setup(parser)

        subparsers = m.let(
            "subparsers", parser.add_subparsers(title="subcommands", dest="subcommand")
        )
        m.setattr(subparsers, "required", True)  # for py3.6
        m.sep()

        for original_fn in self.functions:
            fn = m.let("fn", m.symbol(original_fn))
            sub_parser = m.let(
                "sub_parser",
                subparsers.add_parser(
                    m.getattr(fn, "__name__"), help=m.getattr(fn, "__doc__")
                ),
            )
            Injector(original_fn).inject(sub_parser, callback=m.stmt)
            m.stmt(sub_parser.set_defaults(subcommand=fn))
            m.sep()

        args = m.let("args", parser.parse_args(argv))
        params = m.let("params", m.symbol(vars)(args).copy())

        if not ignore_logging:
            customize.logging_activate(params)

        return cont(params=params)
