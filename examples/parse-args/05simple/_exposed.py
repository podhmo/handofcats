
from typing import Optional

def run(file_name: str, *, nick_name: Optional[str] = None) -> None:
    pass


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', help='-')
    parser.add_argument('--nick-name', required=False, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
