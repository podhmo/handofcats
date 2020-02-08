from handofcats import as_subcommand


@as_subcommand
def hello(*, name="world") -> str:
    return f"hello, {name}"


@as_subcommand
def byebye(*, name="world") -> str:
    return f"byebye, {name}"


as_subcommand.run()
