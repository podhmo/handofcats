from __future__ import annotations
import typing as t
import os

def run(filename: str) -> None:
    pass


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('filename', help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = run
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)  # type: ignore
    return action(**params)


if __name__ == '__main__':
    main()
