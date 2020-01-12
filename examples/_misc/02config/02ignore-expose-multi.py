from handofcats import as_subcommand, Config


@as_subcommand
def hello():
    print("hello")


@as_subcommand
def byebye():
    print("byebye")


as_subcommand.run(config=Config(ignore_expose=True))
