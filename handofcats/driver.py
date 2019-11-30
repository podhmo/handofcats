from .injector import Injector


class Driver:
    def create_injector(self, fn):
        return Injector(fn)

    def create_parser(self, fn, *, argv=None, description=None):
        if "--expose" in (argv or []):
            from .parsers import expose

            inplace = "--inplace" in (argv or [])
            typed = "--typed" in (argv or [])
            description = description or fn.__doc__
            parser = expose.create_parser(
                fn, description=description, inplace=inplace, typed=typed
            )
        else:
            from .parsers import commandline

            parser = commandline.create_parser(
                fn, description=description or fn.__doc__
            )
            parser.add_argument(
                "--expose", action="store_true"
            )  # xxx (for ./expose.py)
            parser.add_argument(
                "--inplace", action="store_true"
            )  # xxx (for ./expose.py)
            parser.add_argument("--typed", action="store_true")  # xxx (for ./expose.py)
        return parser

    def run(self, fn, argv=None):
        parser = self.create_parser(fn, argv=argv, description=fn.__doc__)

        injector = self.create_injector(fn)
        injector.inject(parser)

        args = parser.parse_args(argv)
        params = vars(args).copy()
        params.pop("expose", None)  # xxx: for ./parsers/expose.py
        params.pop("inplace", None)  # xxx: for ./parsers/expose.py
        params.pop("typed", None)  # xxx: for ./parsers/expose.py
        return fn(**params)
