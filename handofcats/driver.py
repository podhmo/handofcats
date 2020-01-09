import typing as t
from .injector import Injector
from . import injectlogging

TargetFunction = t.Callable[..., t.Any]


class Driver:
    def __init__(self, *, ignore_logging=False, description: t.Optional[str] = None):
        self.ignore_logging = ignore_logging
        self.description = description

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
        from .parsers import commandline

        fn = executor.fn
        parser = commandline.create_parser(
            prog=fn.__name__, description=self.description or fn.__doc__
        )
        parser.add_argument("--expose", action="store_true")  # xxx (for ./expose.py)
        parser.add_argument("--inplace", action="store_true")  # xxx (for ./expose.py)
        parser.add_argument("--typed", action="store_true")  # xxx (for ./expose.py)
        return executor.execute(parser, argv, ignore_logging=self.ignore_logging)

    def _run_expose_action(
        self, executor: "Executor", argv: t.Optional[str] = None,
    ) -> t.Any:
        from .parsers import expose

        fn = executor.fn

        inplace = "--inplace" in (argv or [])
        typed = "--typed" in (argv or [])
        description = self.description or fn.__doc__

        # fix:
        parser = expose.create_parser(
            fn, description=description, inplace=inplace, typed=typed
        )
        # TODO: use mock function
        return executor.execute(parser, argv, ignore_logging=self.ignore_logging)


class Executor:
    def __init__(self, fn: TargetFunction) -> None:
        self.fn = fn

    def create_injector(self):
        return Injector(self.fn)

    def execute(
        self,
        parser,
        argv=None,
        *,
        ignore_logging=False,
        cont: t.Optional[TargetFunction] = None
    ):
        cont = cont or self.fn

        injector = self.create_injector()
        injector.inject(parser)

        if not ignore_logging:
            injectlogging.setup(parser)

        args = parser.parse_args(argv)
        params = vars(args).copy()

        if not ignore_logging:
            injectlogging.activate(params)

        params.pop("expose", None)  # xxx: for ./parsers/expose.py
        params.pop("inplace", None)  # xxx: for ./parsers/expose.py
        params.pop("typed", None)  # xxx: for ./parsers/expose.py
        return cont(**params)
