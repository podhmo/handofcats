help
```console
$ handofcats sum.py:sum -h
usage: sum [-h] [--expose] [--inplace] [--typed]
           [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
           x y

positional arguments:
  x                     -
  y                     -

optional arguments:
  -h, --help            show this help message and exit
  --expose              dump generated code. with --inplace, eject from handofcats dependency (default: False)
  --inplace             overwrite file (default: False)
  --typed               typed expression is dumped (default: False)
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
def sum(x: int, y: int) -> None:
    print(f"{x} + {y} = {x + y}")

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=sum.__name__, description=sum.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help
    parser.add_argument('x', type=int, help='-')
    parser.add_argument('y', type=int, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return sum(**params)


if __name__ == '__main__':
    main()
```
