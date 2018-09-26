handofcats
========================================

.. image:: https://travis-ci.org/podhmo/handofcats.svg
  :target: https://travis-ci.org/podhmo/handofcats.svg


A tiny Converter that making executable command script from python function.
If the function is type annotated, it is also used.

Please using `as_command()` decorator.


as_command()
----------------------------------------

greeting.py

.. code-block:: python

  from handofcats import as_command

  @as_command
  def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
      """greeting message"""
      suffix = "!" if is_surprised else ""
      print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


.. code-block:: console

  $ python greeting.py -h
  usage: greeting.py [-h] [--expose] [--is-surprised] [--name NAME] message

  greeting message

  positional arguments:
    message

  optional arguments:
    -h, --help      show this help message and exit
    --expose
    --is-surprised
    --name NAME     (default: 'foo')

  $ python greeting.py hello
  foo: hello
  $ python greeting.py --is-surprised hello
  foo: hello!
  $ python greeting.py --is-surprised --name=bar bye
  bar: bye!

(TODO: detail description)

`--expose`
----------------------------------------

calling with `--expose` option, generationg the code that dropping dependencies of handofcats module.

.. code-block:: console

  $ python greeting.py --expose
  def greeting(message: str, is_surprised: bool = False, name: str = "foo") -> None:
      """greeting message"""
      suffix = "!" if is_surprised else ""
      print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))

  def main(argv=None):
      import argparse
      parser = argparse.ArgumentParser(description='greeting message')
      parser.print_usage = parser.print_help
      parser.add_argument('message')
      parser.add_argument('--is-surprised', action='store_true')
      parser.add_argument('--name', default='foo', required=False)
      args = parser.parse_args(argv)
      greeting(**vars(args))


  if __name__ == '__main__':
      main()


`--inplace`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With `inplace` option, when `--expose`, overwrite target source.

`handofcats` command
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
  usage: handofcats [-h] [--expose] x y

  positional arguments:
    x
    y

  optional arguments:
    -h, --help  show this help message and exit
    --expose

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

  from typing import NewType

  DumpFormat = NewType("DumpFormat", str)
  DumpFormat.choices = ["json", "csv"]   # this: (experimental)


  def run(*, format: DumpFormat = "json"):
      # treated as
      # parser.add_argument("--format", defaul="json", choices=("json", "csv"), required=False)
      ...
