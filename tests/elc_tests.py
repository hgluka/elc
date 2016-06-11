#!/usr/bin/env python
from nose.tools import *
from elc.elc import *

def test_parser():
    parser = Parser()
    assert_equals(parser.parse_eval("{+ 3 5}"), parser.arg_tuple(arg_type='value', value=8))

def test_env():
    pass
