help
```console
$ python greeting.py -h
usage: greeting [-h] [--is-surprised] [--name NAME] [--expose] [--inplace]
                [--simple]
                [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                message

greeting message

positional arguments:
  message               -

options:
  -h, --help            show this help message and exit
  --is-surprised        - (default: False)
  --name NAME           - (default: foo)
  --expose              dump generated code. with --inplace, eject from handofcats dependency (default: False)
  --inplace             overwrite file (default: False)
  --simple              use minimum expression (default: False)
  --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
```
run
```console
$ python greeting.py --is-surprised hello
foo: hello!
```
`--expose`
```console
$ python greeting.py --expose | tee greeting-exposed.py
import typing as t
import os

def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
    """greeting message"""
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(prog=greeting.__name__, description=greeting.__doc__, formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    parser.add_argument('message', help='-')
    parser.add_argument('--is-surprised', action='store_true', help='-')
    parser.add_argument('--name', required=False, default='foo', help='-')
    args = parser.parse_args(argv)
    params = vars(args).copy()
    action = greeting
    if bool(os.getenv("FAKE_CALL")):
        from inspect import getcallargs
        from functools import partial
        action = partial(getcallargs, action)
    return action(**params)


if __name__ == '__main__':
    main()
```
