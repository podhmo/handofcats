
def run(file_name: str) -> None:
    """
# Title

itemize

 1. aaa
 2. bbb
 3. ccc

## Section

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    pass



from typing import Optional, List  # noqa: E402


def main(argv: Optional[List[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__)
    parser.print_usage = parser.print_help
    parser.add_argument('file_name')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
