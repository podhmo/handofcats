help
```console
$ python greeting.py -h
usage: greeting [-h] [--expose] [--inplace] [--typed] [--is-surprised]
                [--name NAME]
                [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                message

greeting message

positional arguments:
  message

optional arguments:
  -h, --help            show this help message and exit
  --expose
  --inplace
  --typed
  --is-surprised
  --name NAME           (default: 'foo')
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


def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
    """greeting message"""
    suffix = "!" if is_surprised else ""
    print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))

def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(prog=greeting.__name__, description=greeting.__doc__)
    parser.print_usage = parser.print_help

    parser.add_argument('message')
    parser.add_argument('--is-surprised', action='store_true')
    parser.add_argument('--name', required=False, default='foo', help="(default: 'foo')")

    args = parser.parse_args(argv)
    params = vars(args).copy()
    return greeting(**params)


if __name__ == '__main__':
    main()
```
