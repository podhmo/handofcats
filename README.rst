handofcats
========================================

A tiny Converter that making executable command script from python function.
If the function has sphinx autodoc style docstring, it is also used.

this module has two functions.

- as_command()
- describe()

If you just convert python function to executable command, then use `as_command()`.
And, you want to show a list of managemented commands, `describe()` is helpful.

as_command()
----------------------------------------

.. code-block:: python

  # greeting.py
  from handofcats import as_command

  @as_command
  def greeting(message, is_surprised=False, name="foo"):
      suffix = "!" if is_surprised else ""
      print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


.. code-block:: bash

  $ python greeting.py
  usage: greeting.py [-h] [--is-surprised] [--name NAME] [-v] [-q] message
  greeting.py: error: too few arguments
  $ python greeting.py -h
  usage: greeting.py [-h] [--is-surprised] [--name NAME] [-v] [-q] message

  positional arguments:
    message

  optional arguments:
    -h, --help      show this help message and exit
    --is-surprised
    --name NAME
    -v, --verbose   (default option: increment logging level(default is WARNING))
    -q, --quiet     (default option: decrement logging level(default is WARNING))
  $ python greeting.py hello
  foo: hello
  $ python greeting.py --is-surprised hello
  foo: hello!
  $ python greeting.py --is-surprised --name=bar bye
  bar: bye!

with docstring (additional feature)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from handofcats import as_command


  @as_command
  def greeting(message, is_surprised=False, name="foo"):
      """ greeting message

      :param message: message of greeting
      :param is_surprised: surprised or not (default=False)
      :param name: name of actor
      """
      suffix = "!" if is_surprised else ""
      print("{name}: {message}{suffix}".format(name=name, message=message, suffix=suffix))


.. code-block:: bash

  $ python greeting.py -h
  usage: greeting.py [-h] [--is-surprised] [--name NAME] [-v] [-q] message

  greeting message

  positional arguments:
    message         message of greeting

  optional arguments:
    -h, --help      show this help message and exit
    --is-surprised  surprised or not (default=False)
    --name NAME     name of actor
    -v, --verbose   (default option: increment logging level(default is
                    WARNING))
    -q, --quiet     (default option: decrement logging level(default is
                    WARNING))


describe()
----------------------------------------

.. code-block:: bash

  $ tree foo/
  foo/
  ├── __init__.py
  ├── __main__.py
  ├── bye.py
  └── hello.py

  $ cat foo/__main__.py
  from handofcats import describe
  describe()

  $ python -m foo
  avaiable commands are here. (with --full option, showing full text)

  - foo.bye
  - foo.hello -- hello message

  $ cat foo/hello.py
  from handofcats import as_command


  @as_command
  def hello():
      """
      hello message
      """
      print("hello")

