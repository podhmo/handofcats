

def main(name: str) -> None:
    pass

def Main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('name')
    args = parser.parse_args(argv)
    main(**vars(args))


if __name__ == '__main__':
    Main()
