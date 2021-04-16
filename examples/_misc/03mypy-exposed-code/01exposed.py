import typing as t
import os



def hello(*, name: str = "world", nickname: t.Optional[str] = None) -> None:
    print(f"hello, {name}")


def byebye(*, args: t.List[str]) -> None:
    print(f"byebye, {', '.join(args)}")


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.required = True

    fn = hello
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__, formatter_class=parser.formatter_class)
    sub_parser.print_usage = sub_parser.print_help  # type: ignore
    sub_parser.add_argument('--name', required=False, default='world', help='-')
    sub_parser.add_argument('--nickname', required=False, help='-')
    sub_parser.set_defaults(subcommand=fn)

    fn = byebye  # type: ignore
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__, formatter_class=parser.formatter_class)
    sub_parser.print_usage = sub_parser.print_help  # type: ignore
    sub_parser.add_argument('--args', required=True, action='append', help='-')
    sub_parser.set_defaults(subcommand=fn)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = params.pop('subcommand')
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)
    return action(**params)


if __name__ == '__main__':
    main()
