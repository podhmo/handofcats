import typing as t
import sys
import re
import inspect
import functools
from prestring.naming import titleize
from prestring.utils import LazyArgumentsAndKeywords, UnRepr
from prestring.python import Module
from ._callback import CallbackArgumentParser

History = t.List[t.Dict[str, t.Any]]


def _make_args(history: History, *, default: str = ""):
    name = history["name"]
    if name == "__init__":
        name = default
    kwargs = {
        k: (repr(v) if k != "type" else v.__name__)
        for k, v in history["kwargs"].items()
    }
    args = [repr(v) for v in history["args"]]
    return f"{name}({LazyArgumentsAndKeywords(args, kwargs)})"


def emit_main(
    m: Module,
    fn: t.Callable,
    history: History,
    *,
    outname: str = "main",
    typed: bool = False,
):
    if typed:
        m.sep()
        m.from_("typing").import_("Optional, List  # noqa: E402")
        m.sep()
        mdef = m.def_(outname, "argv: Optional[List[str]] = None", return_type="None")
    else:
        mdef = m.def_(outname, "argv=None")

    with mdef:
        m.import_("argparse")
        m.stmt(f"parser = argparse.ArgumentParser{_make_args(history[0])}")
        m.stmt("parser.print_usage = parser.print_help")
        for x in history[1:-1]:
            m.stmt(f"parser.{_make_args(x)}")

        history[-1] = {
            "name": history[-1]["name"],
            "args": (UnRepr("argv"),),
            "kwargs": {},
        }  # xxx

        m.stmt(f"args = parser.{_make_args(history[-1])}")
        m.stmt(f"{fn.__name__}(**vars(args))")

    with m.if_("__name__ == '__main__'"):
        m.stmt("{}()", outname)


def print_argparse_code(fn: t.Callable, history: History, *, outname: str = "main"):
    if fn.__name__ == outname:
        outname = titleize(outname)  # main -> Main

    # xxx: is inplace?
    inplace = False
    if "inplace" in history[0]["kwargs"]:
        inplace = history[0]["kwargs"].pop("inplace")
    # xxx: is typed?
    typed = False
    if "typed" in history[0]["kwargs"]:
        typed = history[0]["kwargs"].pop("typed")

    m = Module()
    emit_main(m, fn, history, outname=outname, typed=typed)

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


create_parser = functools.partial(CallbackArgumentParser, print_argparse_code)
