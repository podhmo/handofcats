help
```console
$ handofcats dump.py:runusauusage: psum [-h] [--ys YS] [--expose] [--inplace] [--untyped]
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
(default: False)
  --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
```
run
```console
$ handofcats sum.py:psum [
  {
Σ [10, 20] = 30
handofcats sum.py:psum 10 20 --ys 1 --ys 2
Σ [10, 20] = 30
Σ [10, 20] + Σ [1, 2] = 33
n -W ignorename,age
foo,20
bar,21
 --format=csv
name,age
foo,20
bar,21
```
`--expose`
```console
$ handofcats sum.py:psum --expose | tee sum-exposed.pyimimport typing as t

def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
    """greeting message"""
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=greeting.__name__, description=greeting.__doc__, formatter_class=type('_HelpFormatter', [argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter], {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('message', help='-')
    parser.add_argument('--is-surprised', action='store_true', help='-')
    parser.add_argument('--name', required=False, default='foo', help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    return greeting(**params)


if __name__ == '__main__':
    main()
```
