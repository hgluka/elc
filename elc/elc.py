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
            re.compile('\+').search:'add',
            re.compile('-^>').search:'sub',
            re.compile('\/').search:'div',
            re.compile('\%').search:'mod',
            re.compile('\*').search:'mul',
            re.compile('\|').search:'head',
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
            ('add',): 'binary_op',
            ('sub',): 'binary_op',
            ('div',): 'binary_op',
            ('mod',): 'binary_op',
            ('mul',): 'binary_op',
            ('head',): 'binary_op',

            ('word',): 'expr',
            ('string',): 'expr',
            ('integer',): 'expr',
            ('binary_operation',): 'expr',
            ('func_decl',): 'expr',
            ('func_appl',): 'expr',
            ('bool',): 'expr',
            ('open_bracket', 'expr', 'closed_bracket'): 'expr',
            ('expr', 'expr_sep', 'expr'): 'expr',

            ('expr', 'binary_op', 'expr'): 'binary_operation',

            ('lambda', 'func_name', 'arg_name', 'lambda_dot', 'expr'): 'func_decl',
            ('expr', 'expr'): 'func_appl',


            ('expr', 'equality', 'expr'): 'bool',
            ('expr', 'or', 'expr'): 'bool',
            ('expr', 'and', 'expr'): 'bool'
        }

    def tokenize(self, string):
        token_list = list()
        for i in re.findall('\"[^\"]*\"|->|==|[\_\+\-\.\,\!\?\:\@\#\$\%\^\&\*\(\)\;\\\/\|\<\>\']|[\w]+', string):
            token_list.append(i)
        return token_list

    def token_lookup(self, token):
        for pattern in self.token_table:
            if pattern(token):
                if self.token_table[pattern] in ['string', 'integer', 'equality', 'and', 'or', 'add', 'sub', 'div', 'mod', 'mul', 'head']:
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
            # add rule that makes conflicts with binary operations go away.
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
        self.lambda_node = nt('fun', 'func_name arg_name body')
        def apply_node_c(func_name, arg_name):
            apply_node_type = nt(func_name, 'arg_name')
            return apply_node_type(arg_name)
        self.apply_node = apply_node_c

        def bool_node_c(lhs, rel, rhs):
            bool_node_type = nt(rel, 'lhs rhs')
            return bool_node_type(lhs, rhs)
        self.bool_node = bool_node_c

        def bin_op_node_c(lhs, op, rhs):
            bin_op_node_type = nt(op, 'lhs rhs')
            return bin_op_node_type(lhs, rhs)
        self.bin_op_node = bin_op_node_c

    def convert_node(self, node):
        if node.t_type == 'binary_operation':
            return self.bin_op_node(self.convert_node(node.contents[0]), node.contents[1].contents[0].t_type+'_', self.convert_node(node.contents[2]))
        elif node.t_type == 'func_decl':
            return self.lambda_node(node.contents[1].contents, node.contents[2].contents, self.convert_node(node.contents[4]))
        elif node.t_type == 'func_appl':
            return self.apply_node(node.contents[0].contents[0].contents, self.convert_node(node.contents[1]))
        elif node.t_type == 'bool':
            return self.bool_node(self.convert_node(node.contents[0]), node.contents[1].contents+'_', self.convert_node(node.contents[2]))
        elif node.t_type in ['word', 'integer', 'string']:
            return node.contents
        elif node.t_type == 'expr':
            ret_node = tuple(self.convert_node(i) for i in node.contents if i.contents)
            if len(ret_node)==1:
                ret_node = ret_node[0]
            return ret_node

    def convert_tree(self, cst):
        return self.convert_node(cst[0])

if __name__ == '__main__':
    print('elc v0.3')
    print('by Luka Hadzi-Djokic\n')

    parser = Parser()
    s_a = SemanticAnalyzer()

    while True:
        line = input('> ')
        print(s_a.convert_tree(parser.parse(line)))
