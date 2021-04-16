import typing as t
import os



def hello(*, name: str = "world", nickname: t.Optional[str] = None) -> None:
    print(f"hello, {name}")


def byebye(*, args: t.List[str]) -> None:
    print(f"byebye, {', '.join(args)}")


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=hello.__name__, description=hello.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('--name', required=False, default='world', help='-')
    parser.add_argument('--nickname', required=False, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = hello
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)
    return action(**params)


if __name__ == '__main__':
    main()
