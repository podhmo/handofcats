import sys
import sys as x
import foo.bar
import foo.bar.baz
import foo.bar.baz as b
from i import j  # type: ignore
from i.j import k
from i.j import k as K
from ...xxx import zzz
from yyy.zzz import (
    AAA,
    BBB as bbb,
    CCC,
    DDD,
)
