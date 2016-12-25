#!/usr/bin/env python
from nose.tools import *
from elc.elc import Parser, SemanticAnalyzer

class TestParser():
    def __init__(self):
        self.parser = Parser()
        self.token = self.parser.token

    def test_tokenize(self):
        assert_equals(self.parser.tokenize('( x y "asd fsda" ; 22 )'), ['(', 'x', 'y', '"asd fsda"', ';', '22', ')'])

    def test_lex(self):
        assert_equals(self.parser.lex(['(', 'x', ';', ')', '->', 'fun', 'or', 'and', '[', ']', '==', '"as df"', '123']), [
            self.token(t_type='open_bracket', contents=None),
            self.token(t_type='word', contents='x'),
            self.token(t_type='expr_sep', contents=None),
            self.token(t_type='closed_bracket', contents=None),
            self.token(t_type='lambda_dot', contents=None),
            self.token(t_type='lambda', contents=None),
            self.token(t_type='or', contents='or'),
            self.token(t_type='and', contents='and'),
            self.token(t_type='open_sq_bracket', contents=None),
            self.token(t_type='closed_sq_bracket', contents=None),
            self.token(t_type='equality', contents='=='),
            self.token(t_type='string', contents='"as df"'),
            self.token(t_type='integer', contents='123')
        ])

    def test_parser(self): #should test parser.bottom_up_parse separately
        assert_equals(self.parser.parse('f x'), [
            self.token(t_type='expr', contents=[
                self.token(t_type='func_appl', contents=[
                    self.token(t_type='expr', contents=[
                        self.token(t_type='word',
                                   contents='f')]),
                    self.token(t_type='expr',contents=[
                        self.token(t_type='word',
                                   contents='x')
                    ])
                ])
            ])
        ])

        assert_equals(self.parser.parse('fun f x -> x'), [
            self.token(t_type='expr', contents=[
                self.token(t_type='func_decl', contents=[
                    self.token(t_type='lambda',
                               contents=None),
                    self.token(t_type='func_name',
                               contents='f'),
                    self.token(t_type='arg_name',
                               contents='x'),
                    self.token(t_type='lambda_dot',
                               contents=None),
                    self.token(t_type='expr', contents=[
                        self.token(t_type='word',
                                   contents='x')
                    ])
                ])
            ])
        ])

        assert_equals(self.parser.parse('( x )'), [
            self.token(t_type='expr', contents=[
                self.token(t_type='open_bracket',
                           contents=None),
                self.token(t_type='expr', contents=[
                    self.token(t_type='word',
                               contents='x')]),
                self.token(t_type='closed_bracket',
                           contents=None)
            ])
        ])

        assert_equals(self.parser.parse('x'), [
            self.token(t_type='expr', contents=[
                self.token(t_type='word',
                           contents='x')
            ])
        ])

        assert_equals(self.parser.parse('x or y'), [
            self.token(t_type='expr', contents=[
                self.token(t_type='bool', contents=[
                    self.token(t_type='expr', contents=[
                        self.token(t_type='word',
                                   contents='x')]),
                    self.token(t_type='or', contents='or'),
                    self.token(t_type='expr', contents=[
                        self.token(t_type='word',
                                   contents='y')
                    ])
                ])
            ])
        ])

        assert_equals(self.parser.parse('x ; y'), [
            self.token(t_type='expr', contents=[
                self.token(t_type='expr', contents=[
                    self.token(t_type='word',
                               contents='x')]),
                self.token(t_type='expr_sep',
                           contents=None),
                self.token(t_type='expr', contents=[
                    self.token(t_type='word',
                               contents='y')
                ])
            ])
        ])
