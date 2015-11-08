# -*- coding:utf-8 -*-
import sys
# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes
    long = int
else:
    import types
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    long = long

# base64:
if not PY3:
    import base64
    base64.decodebytes = base64.decodestring


def text_(s, encoding='utf-8', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s  # pragma: no cover


def bytes_(s, encoding='utf-8', errors='strict'):
    """ If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, text_type):  # pragma: no cover
        return s.encode(encoding, errors)
    return s


def write_bytes(out, v):
    out.write(bytes_(text_(v)))


def write_text(out, v):
    out.write(text_(v))

if PY3:
    write = write_text
else:
    write = write_bytes

if not PY3:
    input = raw_input
