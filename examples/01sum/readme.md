help
```console
handofcats sum.py:sum -h
usage: handofcats [-h] [--expose] [--inplace] x y

positional arguments:
  x
  y

optional arguments:
  -h, --help  show this help message and exit
  --expose
  --inplace
```
run
```console
handofcats sum.py:sum 10 20
10 + 20 = 30
```
--expose
```console
handofcats sum.py:sum --expose | tee sum-exposed.py
def sum(x: int, y: int) -> None:
    print(f"{x} + {y} = {x + y}")

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    args = parser.parse_args(argv)
    sum(**vars(args))


if __name__ == '__main__':
    main()
```
