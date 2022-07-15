from typing import overload
import json

import logging
log = logging.getLogger('test')


class A(dict):
    value_1 = "first"
    value_2 = 21
    def __init__(self, *vargs, **kwargs):
        log.debug("vargs: " + str(vargs))
        log.debug("kwargs: "+ str(kwargs))
        # if type(vargs[0]) == dict:
            # pass

def test_class_inherit():
    a = A({"hello": "world"})
    b = A()
    c = A(what="is this")
    # log.debug(a)

class B:
    def __init__(self, num):
        self.num = num;
    @classmethod
    def with_num(cls, num):
        l = []
        for i in range(num):
            l.append(cls(i))
        return l

def test_class_method():
    log.debug(B.with_num(3))
    log.debug([i.num for i in B.with_num(3)])
    