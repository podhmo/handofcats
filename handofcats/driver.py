import typing as t
import sys
from .injector import Injector
from .actions import TargetFunction, ContFunction
from . import injectlogging


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

        m, parser, cont = commandline.setup(fn)
        return self._run(
            m, parser, fn, argv, ignore_logging=self.ignore_logging, cont=cont
        )

    def _run_expose_action(
        self, fn: TargetFunction, argv: t.Optional[str] = None
    ) -> t.Any:
        from .actions import codegen

        inplace = "--inplace" in (argv or [])
        typed = "--typed" in (argv or [])

        m, parser, cont = codegen.setup(fn, inplace=inplace, typed=typed)
        return self._run(m, parser, fn, argv, ignore_logging=True, cont=cont)

    def _run(
        self,
        m,
        parser,
        fn: TargetFunction,
        argv=None,
        *,
        ignore_logging=False,
        cont: t.Optional[ContFunction] = None,
    ):
        cont = cont or fn

        injector = self.injector_class(fn)
        injector.inject(parser, callback=m.stmt)

        # TODO: include generated code, emitted by `--expose`
        if not ignore_logging:
            injectlogging.setup(parser)

        args = parser.parse_args(argv)
        params = vars(args).copy()

        if not ignore_logging:
            injectlogging.activate(params)

        return cont(params=params)


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
            injectlogging.setup(parser)

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
            injectlogging.activate(params)

        return cont(params=params)
