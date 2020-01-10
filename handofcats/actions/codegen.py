import typing as t
import sys
import re
import inspect
from functools import partial
from prestring.naming import titleize
from . import TargetFunction, ContFunction, ArgumentParser
from ._codeobject import Module

History = t.List[t.Dict[str, t.Any]]


def main_code(
    m: Module, fn: t.Callable, *, outname: str = "main", typed: bool = False,
) -> t.Tuple[Module, ArgumentParser]:
    if fn.__name__ == outname:
        outname = titleize(outname)  # main -> Main

    if typed:
        m.sep()
        m.from_("typing").import_("Optional, List  # noqa: E402")
        m.sep()
        mdef = m.def_(outname, "argv: Optional[List[str]] = None", return_type="None")
    else:
        mdef = m.def_(outname, "argv=None")

    with mdef:
        argparse = m.import_("argparse")
        m.sep()
        parser = m.let(
            "parser",
            argparse.ArgumentParser(
                prog=m.getattr(m.symbol(fn), "__name__"),
                description=m.getattr(m.symbol(fn), "__doc__"),
            ),
        )
        m.setattr(parser, "print_usage", parser.print_help)

        m.sep()
        sm = m.submodule()
        m.sep()

        args = m.let("args", parser.parse_args(m.symbol("argv")))
        _ = m.let("params", m.symbol("vars")(args).copy())
        m.return_(f"{fn.__name__}(**params)")

    with m.if_("__name__ == '__main__'"):
        m.stmt(f"{outname}()")
    return sm, parser


def emit(
    m: Module, fn: TargetFunction, *, inplace: bool = False, **kwargs: t.Any,
):
    target_file = inspect.getsourcefile(fn)
    with open(target_file) as rf:
        source = rf.read()
    rx = re.compile(
        r"(?:^@([\S]+\.)?as_command.*|^.*import as_command.*)\n", re.MULTILINE
    )
    exposed = rx.sub("", "".join(source))

    def _dump(out):
        print(exposed, file=out)
        print(m, file=out)

    if not inplace:
        _dump(sys.stdout)
        sys.exit(0)
    else:
        import tempfile
        import os.path

        outpath = None
        try:
            with tempfile.NamedTemporaryFile("w", dir=".", delete=False) as wf:
                outpath = wf.name
                _dump(wf)
            dirpath = os.path.dirname(target_file) or "."
            os.makedirs(dirpath, exist_ok=True)
            os.rename(outpath, target_file)
            sys.exit(0)
        except Exception as e:
            print("error is occured. rollback (exception={e})".format(e=e))
            with open(target_file, "w") as wf:
                wf.write(source)
        finally:
            if os.path.exists(outpath):
                os.remove(outpath)
        sys.exit(1)


def setup(
    fn: TargetFunction, *, inplace: bool, typed: bool, outname: str = "main",
) -> t.Tuple[Module, ArgumentParser, ContFunction]:
    m = Module()
    m.toplevel = m.submodule()
    sm, parser = main_code(m, fn, outname=outname, typed=typed)
    cont = partial(emit, m, fn, inplace=inplace)
    return sm, parser, cont
