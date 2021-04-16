import typing as t


def hello(*, name: str = "world", nickname: t.Optional[str] = None) -> None:
    print(f"hello, {name}")


def byebye(*, args: t.List[str]) -> None:
    print(f"byebye, {', '.join(args)}")
