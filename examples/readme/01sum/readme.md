help
```console
$ handofcats sum.py:sum -h
usage: sum [-h] [--expose] [--inplace] [--simple]
           [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
           x y

positional arguments:
  x                     -
  y                     -

options:
  -h, --help            show this help message and exit
  --expose              dump generated code. with --inplace, eject from handofcats dependency (default: False)
  --inplace             overwrite file (default: False)
  --simple              use minimum expression (default: False)
  --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
```
run
```console
$ handofcats sum.py:sum 10 20
10 + 20 = 30
```
`--expose`
```console
$ handofcats sum.py:sum --expose | tee sum-exposed.py
import typing as t
import os
def sum(x: int, y: int) -> None:
    print(f"{x} + {y} = {x + y}")


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=sum.__name__, description=sum.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('x', type=int, help='-')
    parser.add_argument('y', type=int, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = sum
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)  # type: ignore
    return action(**params)


if __name__ == '__main__':
    main()
```
