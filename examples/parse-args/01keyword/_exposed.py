
def run(*, file_name: str) -> None:
    pass

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help
    parser.add_argument('--file-name', required=True, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
