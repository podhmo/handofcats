import typing as t
from typing_extensions import Literal

Mode = Literal["a", "w", "r"]
Value = Literal[0, 1, -1]


def run(filename: str, *, mode: t.Optional[Mode] = "r", value: Value) -> None:
    pass

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('filename')
    parser.add_argument('--mode', required=False, default='r', choices=['a', 'w', 'r'], help="(default: 'r')")
    parser.add_argument('--value', required=True, choices=[0, 1, -1])
    args = parser.parse_args(argv)
    run(**vars(args))


if __name__ == '__main__':
    main()
