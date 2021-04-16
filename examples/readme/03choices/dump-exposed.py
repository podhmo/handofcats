import typing as t
import os
import sys



def csv_dump(rows: t.Sequence[dict]) -> None:
    import csv
    w = csv.DictWriter(sys.stdout, ["name", "age"])
    w.writeheader()
    w.writerows(rows)


def json_dump(rows: t.Sequence[dict]) -> None:
    import json
    json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


DumpFormat = t.NewType("DumpFormat", str)
DumpFormat.choices = ["json", "csv"]


def run(*, format: DumpFormat = "json"):
    rows = [
        {
            "name": "foo",
            "age": 20,
        },
        {
            "name": "bar",
            "age": 21,
        },
    ]
    dump = globals()["{}_dump".format(format)]
    dump(rows)


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('--format', required=False, default='json', choices=["'json'", "'csv'"], help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = run
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)  # type: ignore
    return action(**params)


if __name__ == '__main__':
    main()
