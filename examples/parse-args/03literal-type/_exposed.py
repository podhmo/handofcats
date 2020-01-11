
import typing as t
from typing_extensions import Literal

Mode = Literal["a", "w", "r"]
Value = Literal[0, 1, -1]
def run(filename: str, *, mode: t.Optional[Mode] = "r", value: Value) -> None:
    pass

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__)
    parser.print_usage = parser.print_help
    parser.add_argument('filename')
    parser.add_argument('--mode', required=False, default='r', choices=["'a'", "'w'", "'r'"], help="(default: 'r')")
    parser.add_argument('--value', required=True, choices=['0', '1', '-1'], type=int)
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
