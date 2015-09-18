handofcats
========================================

A tiny Converter that making executable command script from python function.
If the function has sphinx autodoc style docstring, it is also used.


tl;dr
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
  usage: greeting.py [-h] [--is_surprised] [--name NAME] message
  greeting.py: error: too few arguments
  $ python greeting.py -h
  usage: greeting.py [-h] [--is_surprised] [--name NAME] message

  positional arguments:
    message

  optional arguments:
    -h, --help      show this help message and exit
    --is_surprised
    --name NAME
  $ python greeting.py hello
  foo: hello
  $ python greeting.py --is_surprised hello
  foo: hello!
  $ python greeting.py --is_surprised --name=bar bye
  bar: bye!

with docstring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
  usage: greeting.py [-h] [--is_surprised] [--name NAME] message

  greeting message

  positional arguments:
    message         message of greeting

  optional arguments:
    -h, --help      show this help message and exit
    --is_surprised  surprised or not (default=False)
    --name NAME     name of actor
