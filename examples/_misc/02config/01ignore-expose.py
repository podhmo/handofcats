from handofcats import as_command, Config


@as_command(config=Config(ignore_expose=True))
def hello():
    print("hello")
