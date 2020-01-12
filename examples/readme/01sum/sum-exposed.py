
def sum(x: int, y: int) -> None:
    print(f"{x} + {y} = {x + y}")


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=sum.__name__, description=sum.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('x', type=int, help='-')
    parser.add_argument('y', type=int, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return sum(**params)


if __name__ == '__main__':
    main()
