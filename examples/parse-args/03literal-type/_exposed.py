import typing as t
from typing_extensions import Literal

Mode = Literal["a", "w", "r"]
Value = Literal[0, 1, -1]
def run(filename: str, *, mode: t.Optional[Mode] = "r", value: Value) -> None:
    pass


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('filename', help='-')
    parser.add_argument('--mode', required=False, default='r', choices=["'a'", "'w'", "'r'"], help='-')
    parser.add_argument('--value', required=True, choices=['0', '1', '-1'], type=int, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
