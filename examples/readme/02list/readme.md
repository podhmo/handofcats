help
```console
$ handofcats sum.py:psum -h
usage: psum [-h] [--ys YS] [--expose] [--inplace] [--untyped]
            [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
            [xs [xs ...]]

positional arguments:
  xs                    - (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --ys YS               - (default: None)
  --expose              dump generated code. with --inplace, eject from handofcats dependency (default: False)
  --inplace             overwrite file (default: False)
  --untyped             untyped expression is dumped (default: False)
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


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=psum.__name__, description=psum.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('xs', type=int, nargs='*', help='-')
    parser.add_argument('--ys', required=False, action='append', type=int, help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return psum(**params)


if __name__ == '__main__':
    main()
```
