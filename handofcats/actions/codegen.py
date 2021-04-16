import typing as t
import sys
import inspect
import logging
import tempfile
import pathlib
from functools import partial
from prestring.naming import titleize
from prestring.python import PythonModule
from prestring.codeobject import CodeObjectModuleMixin
from ..config import Config, default_config
from ..types import TargetFunction, SetupParserFunction


class Module(PythonModule, CodeObjectModuleMixin):
    pass


logger = logging.getLogger(__name__)


def emit(
    m: Module,
    fn: TargetFunction,
    *,
    cleanup_code: t.Callable[[str], str],
    inplace: bool = False,
):
    target_file = inspect.getsourcefile(fn)
    code = pathlib.Path(target_file).read_text()
    cleaned = cleanup_code(code)

    def _dump(out):
        content = cleaned.rstrip()
        if "from __future__ import" not in content:
            if hasattr(m, "toplevel"):
                print(m.toplevel, file=out)
            print(content, file=out)
        else:
            # NOTE: from __future__ import xxx 's position is beginning of file.
            lines = content.split("\n")
            buf = []
            for i, line in enumerate(lines):
                if "from __future__ import" in line:
                    buf.append(line)
                else:
                    break
            print("\n".join(buf), file=out)
            print(m.toplevel, file=out)
            print("\n".join(lines[i:]), file=out)
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
        pathlib.Path(target_file).write_text(code)
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
    config: Config = default_config,
) -> None:
    """generate main() code

    something like

    ```
    def main(argv=None):
        import argparse

        parser = argparse.ArgumentParser(prog=hello.__name__, description=hello.__doc__)
        parser.print_usage = parser.print_help

        # # adding code, by self.setup_parser(). e.g.
        # parser.add_argument('--name', required=False, default='world', help="(default: 'world')")
        # parser.add_argument('--debug', action="store_true")

        args = parser.parse_args(argv)
        params = vars(args).copy()
        action = hello
        return action(**params)

    if __name__ == "__main__":
        main()
    ```
    """
    inplace = config.codegen_config.inplace
    typed = config.codegen_config.typed

    m = Module()
    m.sep()
    m.toplevel = Module()

    if fn.__name__ == outname:
        outname = titleize(outname)  # main -> Main

    if typed:
        # import typing as t
        m.toplevel.import_("typing", as_="t")

        mdef = m.def_(
            outname, "argv: t.Optional[t.List[str]] = None", return_type="t.Any"
        )
    else:
        mdef = m.def_(outname, "argv=None")

    # def main(argv=None):
    with mdef:
        parser, _ = setup_parser(fn, m=m, customizations=[], config=config)

        # args = parser.parse_args(argv)
        args = m.let("args", parser.parse_args(m.symbol("argv")))

        # params = vars(args).copy()
        _ = m.let("params", m.symbol("vars")(args).copy())

        # action = <fn>
        m.stmt(f"action = {fn.__name__}")

        if not config.codegen_config.use_primitive_parser:
            m.toplevel.import_("os")

            # if bool(os.getenv("FAKE_CALL")):
            with m.if_("""bool(os.getenv("FAKE_CALL"))"""):

                # from inspect import getcallargs
                m.from_("inspect", "getcallargs")

                # from functools import partial
                m.from_("functools", "partial")

                # action = partial(getcallargs, action)
                m.stmt("action = partial(getcallargs, action)  # type: ignore")

        # return action(**params)
        m.return_("action(**params)")

    # if __name__ == "__main__":
    with m.if_("__name__ == '__main__'"):
        # main()
        m.stmt(f"{outname}()")

    emit(m, fn, inplace=inplace, cleanup_code=partial(_cleanup_code, typed=typed))


def run_as_multi_command(
    setup_parser: SetupParserFunction[t.List[TargetFunction]],
    *,
    functions: t.List[TargetFunction],
    argv: t.Optional[str] = None,
    outname: str = "main",
    config: Config = default_config,
) -> t.Any:
    """generate main() code

    something like

    ```
    def main(argv=None):
        import argparse

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
        subparsers.required = True

        fn = <fn 1>
        sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
        sub_parser.print_usage = sub_parser.print_help  # type: ignore

        # # adding code, by self.setup_parser(). e.g.
        # parser.add_argument('--name', required=False, default='world', help="(default: 'world')")
        # parser.add_argument('--debug', action="store_true")
        sub_parser.set_defaults(subcommand=fn)

        fn = <fn 2>
        sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
        sub_parser.print_usage = sub_parser.print_help  # type: ignore
        # # adding code, by self.setup_parser(). e.g.
        # sub_parser.add_argument('filename')
        sub_parser.set_defaults(subcommand=fn)

        ...

        args = parser.parse_args(argv)
        params = vars(args).copy()
        action = params.pop('subcommand')
        return action(**params)


    if __name__ == '__main__':
        main()
    ```
    """
    inplace = config.codegen_config.inplace
    typed = config.codegen_config.typed

    m = Module()
    m.sep()
    m.toplevel = Module()

    if outname in [fn.__name__ for fn in functions]:
        outname = titleize(outname)  # main -> Main

    if typed:
        # import typing as t
        m.toplevel.import_("typing", as_="t")

        mdef = m.def_(
            outname, "argv: t.Optional[t.List[str]] = None", return_type="t.Any"
        )
    else:
        mdef = m.def_(outname, "argv=None")

    # def main(argv=None):
    with mdef:
        parser, _ = setup_parser(functions, m=m, customizations=[], config=config)

        # args = parser.parse_args(argv)
        args = m.let("args", parser.parse_args(m.symbol("argv")))

        # params = vars(args).copy()
        params = m.let("params", m.symbol("vars")(args).copy())

        # action = params.pop("subcommand")
        m.let("action", params.pop("subcommand"))

        if not config.codegen_config.use_primitive_parser:
            m.toplevel.import_("os")

            # if bool(os.getenv("FAKE_CALL")):
            with m.if_("""bool(os.getenv("FAKE_CALL"))"""):

                # from inspect import getcallargs
                m.from_("inspect", "getcallargs")

                # from functools import partial
                m.from_("functools", "partial")

                # action = partial(getcallargs, action)
                m.stmt("action = partial(getcallargs, action)")

        # return action(**params)
        m.return_("action(**params)")

    # if __name__ == "__main__":
    with m.if_("__name__ == '__main__'"):
        # main()
        m.stmt(f"{outname}()")

    fake = functions[0]
    emit(m, fake, inplace=inplace, cleanup_code=partial(_cleanup_code, typed=typed))


def _cleanup_code(code: str, *, typed: bool) -> str:
    from prestring.python.parse import (
        parse_string,
        PyTreeVisitor,
        type_repr,
        node_name,
    )
    from lib2to3.pytree import Node
    from ._ast import CollectSymbolVisitor

    ast = parse_string(code)
    visitor = CollectSymbolVisitor()
    visitor.visit(ast)
    imported_symbols = visitor.symbols
    candidates = []

    removed_sym_id_set = set()
    for sym in imported_symbols.values():
        if typed and sym.name == "t" and sym.fullname == "typing":
            removed_sym_id_set.add(sym.id)  # duplicated

        if sym.fullname.startswith("handofcats"):
            removed_sym_id_set.add(sym.id)

        # command
        if sym.fullname == "handofcats.as_command":
            candidates.append(f"@{sym.name}")
        elif sym.fullname == "handofcats":
            candidates.append(f"@{sym.name}.as_command")

        # as subcommand
        if sym.fullname == "handofcats.as_subcommand":
            candidates.append(f"@{sym.name}")
            candidates.append(f"{sym.name}.run(")
        elif sym.fullname == "handofcats":
            candidates.append(f"@{sym.name}.as_subcommand")
            candidates.append(f"{sym.name}.as_subcommand.run(")

        # config
        if sym.fullname == "handofcats.Config":
            candidates.append(f"{sym.name}(")
        elif sym.fullname == "handofcats.config.Config(":
            candidates.append(f"{sym.name}(")
        elif sym.fullname == "handofcats":
            candidates.append(f"{sym.name}.Config(")
        elif sym.fullname == "handofcats.config":
            candidates.append(f"{sym.name}.Config(")

    will_be_removed = []

    class RemoveNodeVisitor(PyTreeVisitor):
        def visit_import_name(self, node: Node) -> t.Optional[bool]:
            if id(node) in removed_sym_id_set:
                will_be_removed.append((type_repr(node.type), node))
            return False

        def visit_import_from(self, node: Node) -> t.Optional[bool]:
            if id(node) in removed_sym_id_set:
                will_be_removed.append((type_repr(node.type), node))
            return False

        def visit_decorator(self, node: Node) -> t.Optional[bool]:
            # remove @as_subcommand
            assert type_repr(node.children[0].value) == "@"
            stmt = str(node)
            for x in candidates:
                if x in stmt:
                    will_be_removed.append((type_repr(node.type), node))
                    return True
            return False

        def visit_simple_stmt(self, node: Node) -> t.Optional[bool]:
            # remove as_subcommand.run

            stmt = str(node)

            # TODO: this code, remove `xxx; as_subcommand.run(); zzz`'s xxx and zzz
            # this is bug.
            for x in candidates:
                if x in stmt:
                    will_be_removed.append((type_repr(node.type), node))
                    return True
            return False  # continue

    RemoveNodeVisitor().visit(ast)

    for typ, node in will_be_removed:
        parent = node.parent
        node.remove()

        if typ == "simple_stmt":
            if not str(parent).strip():
                # TODO: remove node.parent.parent if parent_parent is if statement.
                assert node_name(parent.children[-1]) == "DEDENT"
                parent.children[-1].prefix = "pass\n"

    return str(ast)
