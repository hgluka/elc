#!/usr/bin/env python
from nose.tools import *
from elc.elc import *

def test_parser():
    parser = Parser()
    assert_equals(parser.parse_eval("{+ 3 5}"), parser.fun_tuple(operator=parser.arg_tuple('word', '+'),
                                                          arguments=[parser.arg_tuple('value', 3), parser.arg_tuple('value', 5)]))

    assert_equals(parser.parse_block("{+ 3 5} {+ 2 3}"), parser.block_tuple(evals=[
                  parser.fun_tuple(operator=parser.arg_tuple('word', '+'), arguments=[parser.arg_tuple('value', 3), parser.arg_tuple('value', 5)]),
                  parser.fun_tuple(operator=parser.arg_tuple('word', '+'), arguments=[parser.arg_tuple('value', 2), parser.arg_tuple('value', 3)])]))

def test_env():
    pass
