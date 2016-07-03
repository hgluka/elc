#!/usr/bin/env python
import re
from collections import namedtuple as nt

class Env(object):

    def __init__(self):
        self.builtins = {'+': lambda x,y: x+y,
                         'fun': self.fun}

        self.defined = {}

    def fun(self, *args): # not fully implemented (or tested) [TODO]
        fun_name = args[0]
        variables = []
        body = []
        i = 1
        while (arg[i].__class__.__name__ == 'arg' and arg[i].arg_type == word):
            variables.append(arg)
            i += 1
        if arg[i].__class__.__name__ == 'fun':
            body = arg[i]

        self.defined[fun_name] = (variables, body)


class Parser(object):
    '''
    Used to parse list of lines to an abstract syntax tree,
    in the form of a nested named tuple
    '''

    def __init__(self):
        self.string = r'^"([^"]*)"'
        self.number = r'^\d+\b'
        self.word = r'^[^\s{},"]+'
        self.evaluator = r'^{.*}'
        self.fun_tuple = nt('fun', 'operator arguments')
        self.arg_tuple = nt('arg', 'arg_type value')
        self.env = Env()


    def parse_arg(self, arg):
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
            return self.fun_tuple(operator=func, arguments=[i for i in self.parse_args(eval[1::])]) # separate evaluation from parsing,
                                                                                               # or find another way to make function defs possible

    def parse_args(self, arg_list):
        i=0
        while i in range(len(arg_list)):             # had to switch to while loop
            if '{' in arg_list[i]:                   # because an n-iteration skip is impossible in for loops
                for j in range(i, len(arg_list)):    # unless done with iterators
                    if '}' in arg_list[j]:           # which might be a better option
                        break
                yield self.parse_eval(' '.join(arg_list[i:j+1]))
                i=j+1
            else:
                yield self.parse_arg(arg_list[i])
                i += 1

    ''' to be implemented separately
    def evaluate(self, func_name, args):
        if (func_name not in self.env.builtins or func_name not in self.env.defined):
            return 'Evaluator Error: Evaluator not defined.'
        func = self.env.builtins[func_name]
        arg_vals = [i.value for i in args]
        try:
            return self.parse_arg(str(func(*arg_vals)))
        except TypeError:
            return 'Evaluator Error: Wrong number of arguments given.'       # change error reporting system to be actually useful and easier to maintain
        except AttributeError:
            return 'Evaluator Error: Evaluator given wrong type of argument.'
    '''

if __name__=='__main__':
    print('elc v0.1')
    print('-- -- --')

    parser = Parser()

    while True:
        prog = input('> ')
        print(parser.parse_eval(prog))
