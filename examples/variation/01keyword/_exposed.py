

def run(*, filename: str) -> None:
    pass

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('--filename', required=True)
    args = parser.parse_args(argv)
    run(**vars(args))


if __name__ == '__main__':
    main()
