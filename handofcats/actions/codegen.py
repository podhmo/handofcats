import typing as t
import sys
import re
import inspect
import logging
import tempfile
import pathlib
from prestring.naming import titleize
from ..types import TargetFunction, SetupParserFunction
from ._codeobject import Module

logger = logging.getLogger(__name__)


def emit(
    m: Module,
    fn: TargetFunction,
    *,
    cleanup_code: t.Callable[[str], str],
    inplace: bool = False,
):
    target_file = inspect.getsourcefile(fn)
    source = pathlib.Path(target_file).read_text()
    exposed = cleanup_code(source)

    def _dump(out):
        print(exposed, file=out)
        print(m, file=out)

    if not inplace:
        return _dump(sys.stdout)

    outpath = None
    try:
        with tempfile.NamedTemporaryFile("w", dir=".", delete=False) as wf:
            outpath = pathlib.Path(wf.name)
            _dump(wf)

        # create directory
        pathlib.Path(target_file).parent.mkdir(exist_ok=True)
        return outpath.rename(target_file)
    except Exception as e:
        logger.warn("error is occured. rollback (exception=%r)", e)
        pathlib.Path(target_file).write_text(source)
    finally:
        if outpath and outpath.exists():
            outpath.unlink(missing_ok=True)
    sys.exit(1)


def run_as_single_command(
    setup_parser: SetupParserFunction[TargetFunction],
    *,
    fn: TargetFunction,
    argv: t.Optional[str],
    outname: str = "main",
    inplace: bool = False,
    typed: bool = False,
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

    m = Module()
    m.toplevel = m.submodule()
    if fn.__name__ == outname:
        outname = titleize(outname)  # main -> Main

    if typed:
        m.sep()
        m.from_("typing").import_("Optional, List  # noqa: E402")
        m.sep()
        mdef = m.def_(outname, "argv: Optional[List[str]] = None", return_type="None")
    else:
        mdef = m.def_(outname, "argv=None")

    # def main(argv=None):
    with mdef:
        parser, _ = setup_parser(m, fn, customizations=[])

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

    def cleanup_code(source: str) -> str:
        rx = re.compile(
            r"(?:^@([\S]+\.)?as_command.*|^.*import as_command.*)\n", re.MULTILINE
        )
        return rx.sub("", "".join(source))

    emit(m, fn, inplace=inplace, cleanup_code=cleanup_code)


def run_as_multi_command(
    setup_parser: SetupParserFunction[t.List[TargetFunction]],
    *,
    functions: t.List[TargetFunction],
    argv: t.Optional[str] = None,
    outname: str = "main",
    inplace: bool = False,
    typed: bool = False,
) -> t.Any:
    """ generate main() code

        something like

        ```
        ```
        """

    m = Module()
    m.toplevel = m.submodule()

    if outname in [fn.__name__ for fn in functions]:
        outname = titleize(outname)  # main -> Main

    if typed:
        m.sep()
        m.from_("typing").import_("Optional, List  # noqa: E402")
        m.sep()
        mdef = m.def_(outname, "argv: Optional[List[str]] = None", return_type="None")
    else:
        mdef = m.def_(outname, "argv=None")

    # def main(argv=None):
    with mdef:
        parser, _ = setup_parser(m, functions, customizations=[])

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

    # TODO: FIX-IT (BROKEN)
    def cleanup_code(source: str) -> str:
        rx = re.compile(
            r"(?:^@([\S]+\.)?as_command.*|^.*import as_command.*)\n", re.MULTILINE
        )
        return rx.sub("", "".join(source))

    emit(m, fake, inplace=inplace, cleanup_code=cleanup_code)
