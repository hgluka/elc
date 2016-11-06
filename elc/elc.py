#!/usr/bin/env python
import regex as re
from collections import namedtuple as nt

class Parser(object):
    '''
    Used to parse string to a concrete syntax tree,
    implemented as a nested named tuple.
    '''

    def __init__(self):
        self.token_table = {
            re.compile('fun').search:'lambda',
            re.compile('->').search:'lambda_dot',
            re.compile('\(').search:'open_bracket',
            re.compile('\)').search:'closed_bracket',
            re.compile('\[').search:'open_sq_bracket',
            re.compile('\]').search:'closed_sq_bracket',
            re.compile('==').search:'equality',
            re.compile('and').search:'and',
            re.compile('or').search:'or',
            re.compile(';').search:'expr_sep',
            re.compile('^"([^"]*)"').search:'string',
            re.compile('^\d+$').search:'integer'
            }
        self.token = nt('node', 't_type contents')

        self.grammar_table = {
            ('word',): 'expr',
            ('string',): 'expr',
            ('number',): 'expr',
            ('func_decl',): 'expr',
            ('func_appl',): 'expr',
            ('bool',): 'expr',
            ('open_bracket', 'expr', 'closed_bracket'): 'expr',
            ('expr', 'expr_sep', 'expr'): 'expr',

            ('lambda', 'func_name', 'arg_name', 'lambda_dot', 'expr'): 'func_decl',
            ('expr', 'expr'): 'func_appl',

            ('expr', 'equality', 'expr'): 'bool',
            ('expr', 'or', 'expr'): 'bool',
            ('expr', 'and', 'expr'): 'bool'
        }

    def tokenize(self, string):
        token_list = list()
        for i in re.findall('\"[^\"]*\"|[->]|[\_\+\-\.\,\!\?\:\=\@\#\$\%\^\&\*\(\)\;\\\/\|\<\>\']|[\w]+', string):
            token_list.append(i)
        print('debug token_list: ', token_list, '\n')
        return token_list

    def token_lookup(self, token):
        for pattern in self.token_table:
            if pattern(token):
                if self.token_table[pattern] == 'string' or self.token_table[pattern] == 'integer':
                    return self.token(self.token_table[pattern], token)
                return self.token(self.token_table[pattern], None)
        return self.token('word', token)

    def lex(self, token_list):
        lexd = [self.token_lookup(token) for token in token_list]
        for i in range(1, len(lexd)):
            if lexd[i].t_type == 'word' and lexd[i-1].t_type == 'lambda':
                lexd[i] = self.token('func_name', lexd[i].contents)
            if lexd[i].t_type == 'word' and (lexd[i-1].t_type == 'func_name' or lexd[i-1].t_type == 'arg_name'):
                lexd[i] = self.token('arg_name', lexd[i].contents)
        return lexd

    def grammar_lookup(self, candidates):
        for rule in self.grammar_table:
            if rule == tuple([token.t_type for token in candidates]):
                return [self.token(self.grammar_table[rule], candidates)]
        else:
            return candidates

    def shift(self, parse_stack, lexd_input):
        if lexd_input:
            parse_stack.append(lexd_input.pop(0))
            return True
        else:
            return False

    def reduce(self, parse_stack):
        i = len(parse_stack)-1
        while i >= 0:
            handle = parse_stack[i:]
            parse_stack = parse_stack[:i] + self.grammar_lookup(handle)
            i -= 1
        return parse_stack

    def bottom_up_parse(self, lexd_input):
        parse_stack = list()
        parsed = False
        while not parsed:
            if self.shift(parse_stack, lexd_input):
                while parse_stack != self.reduce(parse_stack):
                    parse_stack = self.reduce(parse_stack)
            else:
                parsed = parse_stack
        return parsed

    def parse(self, string):
        return self.bottom_up_parse(self.lex(self.tokenize(string)))

class SemanticAnalyzer(object):
    '''
    Takes an input in the form of a cst (a tree of nested tuples)
    converts it to ast.
    '''

    def __init__(self):
        self.lambda_node = nt('lambda', 'func_name', 'arg_name', 'body')
        self.apply_node = nt('apply', 'func_name', 'arg_name')

    def convert_node(self, node):
        if node.t_type == 'expr':
            node = convert_node(node.contents)

    def convert_tree(self, cst):
        return convert_node(self, cst)

if __name__ == '__main__':
    print('elc v0.12')
    print('-- -- --')

    parser = Parser()

    while True:
        line = input('> ')
        print(parser.parse(line))
