from handofcats import as_subcommand, Config


@as_subcommand
def hello(*, name: str = "world"):
    print(f"hello {name}")


@as_subcommand
def byebye(*, name: str):
    print(f"byebye {name}")


as_subcommand.run(config=Config(ignore_logging=True))
