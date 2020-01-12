
def run(*filename: str) -> None:
    print(", ".join(filename))



from typing import Optional, List  # noqa: E402


def main(argv: Optional[List[str]] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__)
    parser.print_usage = parser.print_help
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
