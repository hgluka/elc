#!/usr/bin/env python
from nose.tools import *
from elc.elc import *

def test_tokenize():
    parser = Parser()

    assert_equals(parser.tokenize('( x y "asd fsda" ; 22 )'), ['(', 'x', 'y', '"asd fsda"', ';', '22', ')'])

def test_lex():
    parser = Parser()

    assert_equals(parser.lex(['(', 'x', ';', ')', '->', 'fun', 'or', 'and', '[', ']', '==', '"as df"', '123']), [parser.token(t_type='open_bracket', contents=None), parser.token(t_type='word', contents='x'), parser.token(t_type='expr_sep', contents=None), parser.token(t_type='closed_bracket', contents=None), parser.token(t_type='lambda_dot', contents=None), parser.token(t_type='lambda', contents=None), parser.token(t_type='or', contents='or'), parser.token(t_type='and', contents='and'), parser.token(t_type='open_sq_bracket', contents=None), parser.token(t_type='closed_sq_bracket', contents=None), parser.token(t_type='equality', contents='=='), parser.token(t_type='string', contents='"as df"'), parser.token(t_type='integer', contents='123')])

def test_parser():
    parser = Parser()

    assert_equals(parser.parse('f x'), [parser.token(t_type='expr', contents=[parser.token(t_type='func_appl', contents=[parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='f')]), parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='x')])])])])

    assert_equals(parser.parse('fun f x -> x'), [parser.token(t_type='expr', contents=[parser.token(t_type='func_decl', contents=[parser.token(t_type='lambda', contents=None), parser.token(t_type='func_name', contents='f'), parser.token(t_type='arg_name', contents='x'), parser.token(t_type='lambda_dot', contents=None), parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='x')])])])])

    assert_equals(parser.parse('( x )'), [parser.token(t_type='expr', contents=[parser.token(t_type='open_bracket', contents=None), parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='x')]), parser.token(t_type='closed_bracket', contents=None)])])

    assert_equals(parser.parse('x'), [parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='x')])])

    assert_equals(parser.parse('x or y'), [parser.token(t_type='expr', contents=[parser.token(t_type='bool', contents=[parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='x')]), parser.token(t_type='or', contents='or'), parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='y')])])])])

    assert_equals(parser.parse('x ; y'), [parser.token(t_type='expr', contents=[parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='x')]), parser.token(t_type='expr_sep', contents=None), parser.token(t_type='expr', contents=[parser.token(t_type='word', contents='y')])])])

