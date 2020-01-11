import dataclasses
from handofcats.actions._ast import parse_file, CollectSymbolVisitor
from handofcats import as_command


@as_command
def parse(filename: str):
    t = parse_file(filename)
    v = CollectSymbolVisitor()
    v.visit(t)
    D = v.symbols
    for name, sym in D.items():
        sym = dataclasses.replace(sym, id=0)  # for idempotence
        print(f"{name} -- {sym}")
