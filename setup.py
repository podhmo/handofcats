import os
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
    "prestring",
]

docs_extras = []

tests_require = []

testing_extras = tests_require + []

setup(
    name='handofcats',
    version='2.1.0',
    description='python function to command translator',
    long_description=README + '\n\n' + CHANGES,
    # https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='',
    author="podhmo",
    author_email="",
    url="https://github.com/podhmo/handofcats",
    packages=find_packages(exclude=["handofcats.tests", "examples"]),
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
handofcats=handofcats.__main__:main
"""
)
