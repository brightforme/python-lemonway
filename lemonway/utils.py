# -*- coding: utf-8 -*-
import re
from lxml.objectify import ObjectifiedElement


def convert_camel_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def pythonize(obj):
    for k, v in obj.__dict__.items():
        # obj.AttrTest = 3
        # => obj.attr_test = 3
        if k == 'xml':
            continue
        if isinstance(getattr(obj, k), ObjectifiedElement):
            v = pythonize(v)
        setattr(obj, convert_camel_case(k), v)
        delattr(obj, k)
    return obj
