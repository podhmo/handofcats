help
```console
$ python cli.py -h
usage: cli.py [-h] [--expose] [--inplace] [--typed]
              [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
              {hello,byebye} ...

optional arguments:
  -h, --help            show this help message and exit
  --expose
  --inplace
  --typed
  --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}

subcommands:
  {hello,byebye}
    hello
    byebye
```
help ( subcommand )
```console
$ python cli.py hello -h
usage: cli.py hello [-h] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  (default: 'world')
```
run
```console
$ python cli.py hello --name world
hello world
```
