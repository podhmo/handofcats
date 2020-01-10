import typing as t
from .injector import Injector
from .actions import TargetFunction
from . import injectlogging


class Driver:
    def __init__(self, *, ignore_logging=False):
        self.ignore_logging = ignore_logging

    def run(
        self, fn: TargetFunction, argv=None,
    ):
        executor = Executor(fn)
        if "--expose" in (argv or []):
            return self._run_expose_action(executor, argv)
        else:
            return self._run_command_line(executor, argv)

    def _run_command_line(
        self, executor: "Executor", argv: t.Optional[str] = None
    ) -> t.Any:
        from .actions import commandline

        fn = executor.fn
        m, parser, cont = commandline.setup(fn)
        return executor.execute(
            m, parser, argv, ignore_logging=self.ignore_logging, cont=cont
        )

    def _run_expose_action(
        self, executor: "Executor", argv: t.Optional[str] = None,
    ) -> t.Any:
        from .actions import codegen

        fn = executor.fn

        inplace = "--inplace" in (argv or [])
        typed = "--typed" in (argv or [])

        m, parser, cont = codegen.setup(fn, inplace=inplace, typed=typed)
        # TODO: use mock function
        return executor.execute(
            m, parser, argv, ignore_logging=self.ignore_logging, cont=cont
        )


class Executor:
    injector_class = Injector

    def __init__(self, fn: TargetFunction) -> None:
        self.fn = fn

    def execute(
        self,
        m,
        parser,
        argv=None,
        *,
        ignore_logging=False,
        cont: t.Optional[TargetFunction] = None
    ):
        cont = cont or self.fn

        injector = self.injector_class(self.fn)
        injector.inject(parser, callback=m.stmt)

        if not ignore_logging:
            injectlogging.setup(parser)

        args = parser.parse_args(argv)
        params = vars(args).copy()

        if not ignore_logging:
            injectlogging.activate(params)

        return cont(**params)
