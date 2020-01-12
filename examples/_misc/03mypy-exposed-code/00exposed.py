import typing as t


def hello(*, name: str = "world", nickname: t.Optional[str] = None) -> None:
    print(f"hello, world")


def byebye(*, args: t.List[str]) -> None:
    print(f"byebye, {', '.join(args)}")



from typing import Optional, List  # noqa: E402


def main(argv: Optional[List[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(prog=hello.__name__, description=hello.__doc__)
    parser.print_usage = parser.print_help
    parser.add_argument('--name', required=False, default='world', help="(default: 'world')")
    parser.add_argument('--nickname', required=False)
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return hello(**params)


if __name__ == '__main__':
    main()
