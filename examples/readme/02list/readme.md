help
```console
handofcats sum.py:psum -h
usage: handofcats [-h] [--expose] [--inplace] [--typed] [--ys YS]
                  [xs [xs ...]]

positional arguments:
  xs

optional arguments:
  -h, --help  show this help message and exit
  --expose
  --inplace
  --typed
  --ys YS
```
run
```console
handofcats sum.py:psum 10 20
Σ [10, 20] = 30
handofcats sum.py:psum 10 20 --ys 1 --ys 2
Σ [10, 20] = 30
Σ [10, 20] + Σ [1, 2] = 33
```
--expose
```console
handofcats sum.py:psum --expose | tee sum-exposed.py
import typing as t


def psum(xs: t.List[int], *, ys: t.Optional[t.List[int]] = None):
    print(f"Σ {xs} = {sum(xs)}")
    if ys:
        print(f"Σ {xs} + Σ {ys} = {sum(xs) + sum(ys)}")

def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=None)
    parser.print_usage = parser.print_help
    parser.add_argument('xs', type=int, nargs='*')
    parser.add_argument('--ys', required=False, action='append', type=int)
    args = parser.parse_args(argv)
    psum(**vars(args))


if __name__ == '__main__':
    main()
```
