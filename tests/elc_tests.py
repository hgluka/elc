#!/usr/bin/env python
from nose.tools import *
from elc.elc import *

def test_parser():
    parser = Parser()
    assert_equals(parser.parse_eval("{+ 3 5}"), parser.fun_tuple(operator=parser.arg_tuple('word', '+'),
                                                          arguments=[parser.arg_tuple('value', 3), parser.arg_tuple('value', 5)]))

def test_env():
    pass
