
def run(file_name: str) -> None:
    pass

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__)
    parser.print_usage = parser.print_help
    parser.add_argument('file_name')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
