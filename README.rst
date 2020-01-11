handofcats
========================================

.. image:: https://travis-ci.org/podhmo/handofcats.svg
  :target: https://travis-ci.org/podhmo/handofcats.svg


A tiny magically Converter that making executable command script from plain python function.
If the function is type annotated, it is used.

- If you want single command, ``as_command()`` is helpful ✨ 
- If you want multi command has many sub-commands, ``as_subcommand()`` is helpful ✨ 
- If you want something like `create-react-app's eject <https://github.com/facebook/create-react-app#philosophy>`_, use ` ``--expose`` option <https://github.com/podhmo/handofcats#--expose>`_ ◀️ 

``as_command()``
----------------------------------------

greeting.py

.. code-block:: python

  from handofcats import as_command

  @as_command
  def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
      """greeting message"""
      suffix = "!" if is_surprised else ""
      print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


🚀  Using as single command

.. code-block:: console

  $ python greeting.py hello
  foo: hello
  $ python greeting.py --is-surprised hello
  foo: hello!
  $ python greeting.py --is-surprised --name=bar bye
  bar: bye!

help

.. code-block:: console

  $ python greeting.py -h
  usage: greeting [-h] [--is-surprised] [--name NAME] [--expose] [--inplace]
                  [--typed]
                  [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                  message

  greeting message

  positional arguments:
    message

  optional arguments:
    -h, --help            show this help message and exit
    --is-surprised
    --name NAME           (default: 'foo')
    --expose              dump generated code. with --inplace, eject from
                          handofcats dependency
    --inplace             overwrite file
    --typed               typed expression is dumped
    --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}


( :warning: TODO: detail description )


``as_subcommand()`` and ``as_subcommand.run()``
------------------------------------------------------------------------------------------------------------------------

multi command ( the command has sub-commands ) .

cli.py

.. code-block:: python

   from handofcats import as_subcommand


   @as_subcommand
   def hello(*, name: str = "world"):
       print(f"hello {name}")


   @as_subcommand
   def byebye(name):
       print(f"byebye {name}")


   # :warning: don't forget this
   as_subcommand.run()

🚀  Using as multi command

.. code-block:: cosole

   $ python cli.py hello
   hello world

   $ python cli.py hello --name foo
   hello foo

   $ python cli.py byebye foo
   byebye foo

help

.. code-block:: cosole

   $ python cli.py -h
   usage: cli.py [-h] [--expose] [--inplace] [--typed]
                 [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                 {hello,byebye} ...

   optional arguments:
     -h, --help            show this help message and exit
     --expose              dump generated code. with --inplace, eject from
                           handofcats dependency
     --inplace             overwrite file
     --typed               typed expression is dumped
     --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}

   subcommands:
     {hello,byebye}
       hello
       byebye


   $ python cli.py hello -h
   usage: cli.py hello [-h] [--name NAME]

   optional arguments:
     -h, --help   show this help message and exit
     --name NAME  (default: 'world')



``--expose``
----------------------------------------

Runing with ``--expose`` option, generationg the code that dropping dependencies of handofcats module.

Something like `create-react-app's eject <https://github.com/facebook/create-react-app#philosophy>`_ .

> No Lock-In: You can “eject” to a custom setup at any time. Run a single command, and all the configuration and build dependencies will be moved directly into your project, so you can pick up right where you left off.

If you want to eject from `the code described above <https://github.com/podhmo/handofcats#as_command>`_, ``--expose`` is helpful, maybe.

.. code-block:: console

  $ python greeting.py --expose

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

``--expose`` with ``--inplace``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition, running with ``inplace`` option, when ``--expose``, overwrite target source code.

``handofcats`` command
----------------------------------------

sum.py

.. code-block:: python

  def sum(x: int, y: int) -> None:
      print(f"{x} + {y} = {x + y}")

It is also ok, calling the function that not decorated via handofcats command.

.. code-block:: console

  $ handofcats sum.py:sum 10 20
  10 + 20 = 30

  $ handofcats sum.py:sum -h
  handofcats sum.py:sum -h
  usage: sum [-h] [--expose] [--inplace] [--typed]
             [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
             x y

  positional arguments:
    x
    y

  optional arguments:
    -h, --help            show this help message and exit
    --expose              dump generated code. with --inplace, eject from
                          handofcats dependency
    --inplace             overwrite file
    --typed               typed expression is dumped
    --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}

experimental
----------------------------------------

sequences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from typing import List, Optional

  def psum(xs: List[int], *, ys: Optional[List[int]] = None):
      # treated as
      # parser.add_argument('xs', nargs='*', type=int)
      # parser.add_argument('--ys', action='append', required=False, type=int)
      ..

choices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from typing_extensions import Literal


  DumpFormat = Literal["json", "csv"]   # this: (experimental)


  def run(*, format: DumpFormat = "json"):
      # treated as
      # parser.add_argument("--format", defaul="json", choices=("json", "csv"), required=False)
      ...
