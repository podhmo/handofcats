from handofcats import as_command, Config


@as_command(config=Config(ignore_logging=True))
def hello():
    print("hello")
