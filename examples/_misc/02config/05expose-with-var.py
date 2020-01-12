from handofcats import as_subcommand
from handofcats import Config


@as_subcommand
def hello(*, name: str = "world"):
    print(f"hello {name}")


@as_subcommand
def byebye(*, name: str):
    print(f"byebye {name}")


cfg = Config(ignore_logging=True)
if __name__ == "__main__":
    as_subcommand.run(config=cfg)
