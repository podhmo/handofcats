import sys
import typing as t
import typing_extensions as tx

def csv_dump(rows: t.Sequence[dict]) -> None:
    import csv
    w = csv.DictWriter(sys.stdout, ["name", "age"])
    w.writeheader()
    w.writerows(rows)


def json_dump(rows: t.Sequence[dict]) -> None:
    import json
    json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


DumpFormat = tx.Literal["json", "csv"]


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
