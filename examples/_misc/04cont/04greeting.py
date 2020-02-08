import json
from handofcats import as_subcommand, Config


@as_subcommand
def hello(*, name="world") -> str:
    return f"hello, {name}"


@as_subcommand
def byebye(*, name="world") -> str:
    return f"byebye, {name}"


config = Config(cont=lambda x: print(json.dumps(x)))
as_subcommand.run(config=config)
