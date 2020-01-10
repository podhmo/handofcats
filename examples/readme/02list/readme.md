help
```console
$ handofcats sum.py:psum -h
usage: psum [-h] [--expose] [--inplace] [--typed] [--ys YS]
            [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
            [xs [xs ...]]

positional arguments:
  xs

optional arguments:
  -h, --help            show this help message and exit
  --expose
  --inplace
  --typed
  --ys YS
  --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
```
run
```console
$ handofcats sum.py:psum 10 20
Σ [10, 20] = 30
handofcats sum.py:psum 10 20 --ys 1 --ys 2
Σ [10, 20] = 30
Σ [10, 20] + Σ [1, 2] = 33
```
`--expose`
```console
$ handofcats sum.py:psum --expose | tee sum-exposed.py
import typing as t


def psum(xs: t.List[int], *, ys: t.Optional[t.List[int]] = None):
    print(f"Σ {xs} = {sum(xs)}")
    if ys:
        print(f"Σ {xs} + Σ {ys} = {sum(xs) + sum(ys)}")

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=psum.__name__, description=psum.__doc__)
    parser.print_usage = parser.print_help

    parser.add_argument('xs', type=int, nargs='*')
    parser.add_argument('--ys', required=False, action='append', type=int)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    return psum(**params)


if __name__ == '__main__':
    main()
```
