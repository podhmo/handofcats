from handofcats import as_subcommand


@as_subcommand
def hello(*, name: str = "world"):
    print(f"hello {name}")


# FIXME: default arguments (positional arguments)
@as_subcommand
def byebye(name: str):
    print(f"byebye {name}")


# ignored
def ignore(name: str):
    print(f"ignored {name}")


def _ignore(name: str):
    print("of cource, ignored")


as_subcommand.run()
