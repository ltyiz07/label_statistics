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
    