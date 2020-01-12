import typing as t


def hello(*, name: str = "world", nickname: t.Optional[str] = None) -> None:
    print(f"hello, world")


def byebye(*, args: t.List[str]) -> None:
    print(f"byebye, {', '.join(args)}")



from typing import Optional, List  # noqa: E402


def main(argv: Optional[List[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.required = True

    fn = hello
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument('--name', required=False, default='world', help="(default: 'world')")
    sub_parser.add_argument('--nickname', required=False)
    sub_parser.set_defaults(subcommand=fn)

    fn = byebye
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__)
    sub_parser.add_argument('--args', required=True, action='append')
    sub_parser.set_defaults(subcommand=fn)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    subcommand = params.pop('subcommand')
    return subcommand(**params)


if __name__ == '__main__':
    main()
