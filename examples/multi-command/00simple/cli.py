from handofcats.driver import MultiDriver

md = MultiDriver()


@md.register
def hello(*, name: str = "world"):
    print(f"hello {name}")


@md.register
def byebye(name):
    print(f"byebye {name}")


md.run()
