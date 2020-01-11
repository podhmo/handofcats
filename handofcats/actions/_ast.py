import typing as t
import dataclasses
from prestring.python.parse import PyTreeVisitor, type_repr
from prestring.python.parse import parse_file  # noqa
from lib2to3.pytree import Node


# parse imports symbols
@dataclasses.dataclass
class Symbol:
    fullname: str
    name: t.Optional[str] = None
    id: int = 0


def parse_dotted_as_name(node: Node) -> Symbol:
    # <Leaf> as <Leaf>
    assert len(node.children) == 3, str(node.children)

    if type_repr(node.children[0].type) == "dotted_name":
        module = parse_dotted_name(node.children[0])
        assert node.children[1].value == "as"
        name = node.children[2].value.strip()
        return Symbol(fullname=module, name=name)
    else:
        module = node.children[0].value.strip()
        assert node.children[1].value == "as"
        name = node.children[2].value.strip()
        return Symbol(fullname=module, name=name)


def parse_dotted_name(node: Node) -> str:
    # <Leaf> { . <Leaf> }+
    path = []
    for i in range(0, len(node.children), 2):
        path.append(node.children[i].value.strip())
        if i - 1 > 0:
            assert node.children[i - 1].value == "."
    return ".".join(path)


def parse_import_as_name(node: Node) -> str:
    # <Leaf> as <Leaf>
    assert len(node.children) == 3
    module = node.children[0].value.strip()
    assert node.children[1].value == "as"
    name = node.children[2].value.strip()
    return Symbol(fullname=module, name=name)


def parse_import_as_names(node: Node, *, module: str) -> t.List[Symbol]:
    # <Leaf> { , <Leaf> }+
    syms = []
    for i in range(0, len(node.children), 2):
        x = node.children[i]

        if type_repr(x.type) == "import_as_name":
            sym = parse_import_as_name(x)
            sym = Symbol(name=sym.name, fullname=f"{module}.{sym.fullname}")
        else:
            name = x.value.strip()
            sym = Symbol(name=name, fullname=f"{module}.{name}")

        syms.append(sym)
        if i - 1 > 0:
            assert node.children[i - 1].value == ","
    return syms


class CollectSymbolVisitor(PyTreeVisitor):
    def __init__(self):
        self.symbols: t.Dict[str, Symbol] = {}  # name -> fullname

    def visit_import_name(self, node: Node) -> t.Optional[t.Any]:
        # import [ <Leaf> | <dotted_as_name> | <dotted_name> ]
        assert len(node.children) == 2, node.children

        if type_repr(node.children[1].type) == "dotted_as_name":
            sym = parse_dotted_as_name(node.children[1])
            sym.id = id(node)
            self.symbols[sym.name] = sym
        elif type_repr(node.children[1].type) == "dotted_name":
            # <Leaf> { . <Leaf> }+
            module = parse_dotted_name(node.children[1])
            sym = Symbol(name=module, fullname=module)
            sym.id = id(node)
            self.symbols[module] = sym
        else:
            module = node.children[1].value.strip()
            sym = Symbol(name=module, fullname=module)
            sym.id = id(node)
            self.symbols[module] = sym
        return True  # stop

    def visit_import_from(self, node: Node) -> t.Optional[t.Any]:
        assert node.children[0].value == "from"

        module_path = []
        for i, x in enumerate(node.children[1:], 1):
            if type_repr(x.type) == "dotted_name":
                name = parse_dotted_name(x)
            else:
                name = x.value.strip()
                if name == "import":
                    break
            module_path.append(name)
            if name != ".":
                module_path.append(".")
        module_path.pop()
        module = "".join(module_path)

        sym_list = []
        for x in node.children[i + 1 :]:
            if type_repr(x.type) == "import_as_name":
                sym = parse_import_as_name(x)
                sym_list.append(sym)
            elif type_repr(x.type) == "import_as_names":
                syms = parse_import_as_names(x, module=module)
                sym_list.extend(syms)
            elif x.value.strip() == "(":
                continue
            elif x.value.strip() == ")":
                continue
            else:
                name = x.value.strip()
                sym = Symbol(name=name, fullname=f"{module}.{name}")
                sym_list.append(sym)

        # todo: relative
        for sym in sym_list:
            sym.id = id(node)
            self.symbols[sym.name] = sym
        return True  # stop
