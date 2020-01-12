from handofcats import as_command
from handofcats import Config


@as_command(config=Config(ignore_logging=True))
def hello():
    print("hello")
