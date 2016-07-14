#!/usr/bin/env python
import regex
from collections import namedtuple as nt

class Env(object):

    def __init__(self):
        self.builtins = {'+': lambda x,y: x+y,
                         'fun': self.fun}

        self.defined = {}

    def fun(self, *args): # not fully implemented (or tested) [TODO]
        fun_name = args[0]
        variables = []
        i = 1
        while (arg[i].__class__.__name__ == 'arg' and arg[i].arg_type == word):
            variables.append(arg)
            i += 1
        if arg[i].__class__.__name__ == 'fun':
            body = arg[i]
        else:
            return 'Syntax Error: Function body missing'

        return (fun_name, variables, body)


class Parser(object):
    '''
    Used to parse list of lines to an abstract syntax tree,
    in the form of a nested named tuple
    '''

    def __init__(self):
        self.string = r'^"([^"]*)"'
        self.number = r'^\d+\b'
        self.word = r'^[^\s{},"]+'
        self.evaluator = r'^{.*}' # edit to work with both nested and leveled evaluator expressions
        self.block_tuple = nt('block', 'evals')
        self.fun_tuple = nt('fun', 'operator arguments')
        self.arg_tuple = nt('arg', 'arg_type value')


    def parse_arg(self, arg):
        match = regex.match(self.string, arg)
        if (match):
            return self.arg_tuple(arg_type='value', value=match[0])
        match = regex.match(self.number, arg)
        if (match):
            return self.arg_tuple(arg_type='value', value=int(match[0]))
        match = regex.match(self.word, arg)
        if (match):
            return self.arg_tuple(arg_type='word', value=match[0])

    def parse_eval(self, stmt):
        evaluator = regex.match(self.evaluator, stmt)
        ev = evaluator[0][1::]
        ev = ev.split()
        print(ev)
        func = self.parse_arg(ev[0])
        if(func.arg_type != 'word'):
            return 'Syntax Error: Evaluators must start with words.'
        else:
            return self.fun_tuple(operator=func, arguments=[i for i in self.parse_args(ev[1::])])

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

    def parse_program(self, program):
        eval_list = []
        for match in regex.findall(r'{((?:[^{}]|(?R))*)}', program):
            eval_list.append(self.parse_eval('{'+match+'}'))
        return self.block_tuple(eval_list)


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
        print(parser.parse_program(prog))
