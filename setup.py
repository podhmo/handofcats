# -*- coding:utf-8 -*-

import os
import sys


from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
    with open(os.path.join(here, 'CHANGES.txt')) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ''


install_requires = [
    "cached_property"
]

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3
if not PY3:
    install_requires.append("importlib2")


docs_extras = [
]

tests_require = [
]

testing_extras = tests_require + [
]

setup(name='handofcats',
      version='0.4.3',
      description='python function to command translator',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      keywords='',
      author="podhmo",
      author_email="",
      url="https://github.com/podhmo/handofcats",
      packages=find_packages(exclude=["handofcats.tests", "demo"]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'testing': testing_extras,
          'docs': docs_extras,
      },
      tests_require=tests_require,
      license="mit",
      test_suite="handofcats.tests",
      entry_points="""
[console_scripts]
handofcats=handofcats.cli:main
""")
