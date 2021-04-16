import typing as t
import os

def main(name: str) -> None:
    pass


def Main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=main.__name__, description=main.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('name', help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = main
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)
    return action(**params)


if __name__ == '__main__':
    Main()
