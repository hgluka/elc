#!/usr/bin/env python
import re
from collections import namedtuple as nt

class Env(object):

    def __init__(self):
        self.builtins = {'+': [lambda x,y: x+y, 2]}

class Parser(object):

    def __init__(self):
        self.string = r'^"([^"]*)"'
        self.number = r'^\d+\b'
        self.word = r'^[^\s{},"]+'
        self.evaluator = r'^{.*}'
        self.arg_tuple = nt('arg', 'arg_type value')
        self.env = Env()


    def parse_arg(self, arg):              # think about best way to set up an ast
        arg = arg.strip()                  # classes or nested dicts,
                                           # which is faster? which is easier to manipulate?
        arg_dict = {}
        match = re.match(self.string, arg)
        if (match):
            return self.arg_tuple(arg_type='value', value=match.group(1))
        match = re.match(self.number, arg)
        if (match):
            return self.arg_tuple(arg_type='value', value=int(match.group(0)))
        match = re.match(self.word, arg)
        if (match):
            return self.arg_tuple(arg_type='word', value=match.group(0))

    def parse_eval(self, stmt):
        evaluator = re.match(self.evaluator, stmt)
        eval = evaluator.group(0)[1:len(evaluator.group(0))-1]
        eval = eval.split()
        func = self.parse_arg(eval[0])
        if(func.arg_type != 'word'):
            return 'Syntax Error: Evaluators must start with words.'
        else:
           return self.evaluate(func.value, [i for i in self.parse_args(eval[1::])]) # separate evaluation from parsing,
                                                                         # or find another way to make function defs possible

    def parse_args(self, arg_list):
        for i in range(len(arg_list)):
            if '{' in arg_list[i]:
                for j in range(len(arg_list)):
                    if '}' in arg_list[j]:
                        break
                yield self.parse_eval(' '.join(arg_list[i:j]))
            else:
                yield self.parse_arg(arg_list[i])

    def evaluate(self, func_name, args):
        if (func_name not in self.env.builtins): # and (func_name not in self.env.user_defs):
            return 'Evaluator Error: Evaluator not defined.'
        func = self.env.builtins[func_name][0]
        arg_vals = [i.value for i in args]
        try:
            if (self.env.builtins[func_name][1] != len(arg_vals)):
                return 'Evaluator Error: Wrong number of arguments given.'       # change error reporting system to be actually useful
            return self.parse_arg(str(func(*arg_vals)))
        except TypeError:
            return 'Evaluator Error: Evaluator given wrong type of argument.'


if __name__=='__main__':
    print('elc v0.1')
    print('-- -- --')

    parser = Parser()

    while True:
        prog = input('> ')
        print(parser.parse_eval(prog))
