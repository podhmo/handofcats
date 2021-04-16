import sys
import os
import fastentrypoints
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, "README.md")) as f:
        README = f.read()
    with open(os.path.join(here, "CHANGES.txt")) as f:
        CHANGES = f.read()
except IOError:
    README = CHANGES = ""

install_requires = ["prestring>=0.9.0", "typing_extensions", "magicalimport"]
if sys.version_info[:2] <= (3, 6):
    install_requires.append("dataclasses")

docs_extras = []
tests_require = []
dev_extras = ["flake8", "black", "mypy"]
testing_extras = tests_require + dev_extras

setup(
    name="handofcats",
    version=open(os.path.join(here, "VERSION")).read().strip(),
    description="python function to command translator",
    long_description=README + "\n\n" + CHANGES,
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="",
    author="podhmo",
    author_email="",
    url="https://github.com/podhmo/handofcats",
    packages=find_packages(exclude=["handofcats.tests", "examples"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={"testing": testing_extras, "docs": docs_extras, "dev": dev_extras},
    tests_require=tests_require,
    license="mit",
    test_suite="handofcats.tests",
    entry_points="""
[console_scripts]
handofcats=handofcats.cli:main
""",
)
