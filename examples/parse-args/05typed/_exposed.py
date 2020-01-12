from typing import Optional

def run(file_name: str, *, nick_name: Optional[str] = None) -> None:
    pass



from typing import Optional, List  # noqa: E402


def main(argv: Optional[List[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help
    parser.add_argument('file_name', help='-')
    parser.add_argument('--nick-name', required=False, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
