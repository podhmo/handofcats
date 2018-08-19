import logging
import sys
logger = logging.getLogger(__name__)


def as_command(fn=None, argv=None, level=2):
    def call(fn, level=1, argv=argv):
        # caller module extraction, if it is __main__, calling as command
        frame = sys._getframe(level)
        name = frame.f_globals["__name__"]
        if name != "__main__":
            return fn

        from handofcats.parsers import commandline
        parser = commandline.create_parser(fn, description=fn.__doc__)
        args = parser.parse_args()
        params = vars(args).copy()
        return fn(**params)

    if fn is None:
        return call
    else:
        return call(fn, level=level, argv=argv)


# alias
handofcats = as_command
