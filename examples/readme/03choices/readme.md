help
```console
$ python -W ignore -m handofcats dump.py:run -h
usage: run [-h] [--format {json,csv}] [--expose] [--inplace] [--typed]
           [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]

optional arguments:
  -h, --help            show this help message and exit
  --format {json,csv}   (default: 'json')
  --expose
  --inplace
  --typed
  --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
```
run
```console
$ python -W ignore -m handofcats dump.py:run
[
  {
    "name": "foo",
    "age": 20
  },
  {
    "name": "bar",
    "age": 21
  }
]
python -W ignore -m handofcats dump.py:run --format=csv
name,age
foo,20
bar,21
```
`--expose`
```console
$ python -W ignore -m handofcats dump.py:run --expose | tee dump-exposed.py
import sys
import typing as t


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

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=run.__name__, description=run.__doc__)
    parser.print_usage = parser.print_help
    parser.add_argument('--format', required=False, default='json', choices=["'json'", "'csv'"], help="(default: 'json')")
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return run(**params)


if __name__ == '__main__':
    main()
```
