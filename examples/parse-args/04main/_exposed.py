
def main(name: str) -> None:
    pass

def Main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=main.__name__, description=main.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help
    parser.add_argument('name', help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return main(**params)


if __name__ == '__main__':
    Main()
