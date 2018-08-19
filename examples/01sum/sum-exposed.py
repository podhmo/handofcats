def sum(x: int, y: int) -> None:
    print(f"{x} + {y} = {x + y}")

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    args = parser.parse_args(argv)
    sum(**vars(args))


if __name__ == '__main__':
    main()
