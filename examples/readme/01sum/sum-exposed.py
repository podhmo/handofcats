def sum(x: int, y: int) -> None:
    print(f"{x} + {y} = {x + y}")

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=sum.__name__, description=sum.__doc__)
    parser.print_usage = parser.print_help
    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return sum(**params)


if __name__ == '__main__':
    main()
