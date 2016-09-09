#!/usr/bin/env python
import regex
from collections import namedtuple as nt

class Env(object):

    def __init__(self):
        self.builtins = {'+': lambda x,y: x+y,
                         'fun': self.fun}

        self.defined = {}


    def fun(self):
        pass # [TODO] lambda

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
                        break                        # recursive regex or this?
                yield self.parse_eval(' '.join(arg_list[i:j+1]))

                i=j+1
            else:
                yield self.parse_arg(arg_list[i])
                i += 1

    def parse_block(self, program):
        eval_list = []
        for match in regex.findall(r'{((?:[^{}]|(?R))*)}', program):
            eval_list.append(self.parse_eval('{'+match+'}'))
        return self.block_tuple(eval_list)


class Evaluator(object):
    def __init__(self):
        pass

    def get_function_body(self, func, env):
        try:
            function = env.defined[func.operator]
        except KeyError:
            pass # flat is better than nested
        try:
            function = env.builtin[func.oprator]
        except KeyError:
            return 'Function ' + func.operator + 'not defined.'

        return function

    def evaluate(self, node, env):
        if node.__class__.__name__ == 'block':
            for e in node.evals:
                return self.evaluate(e)
        elif node.__class__.__name__ == 'fun':
            arg_list = []
            for arg in node.args:
                arg_list.append(self.evaluate(arg))
            if node.operator in env.defined:
                # replace args in function body with evaluated arg_list, \
                # then recurse over that function
                env.defined[node.operator].args = arg_list
                return evaluate(env.defined[node.operator])
            elif node.operator in env.builtins:
                return env.builtins[node.operator](zip(*arg_list))
            else:
                return 'Function not defined.'
        elif node.__class__.__name__ == 'arg':
            if node.arg_type == 'value':
                return node.value
            elif node.arg_type == 'word':
                if node.value in env.defined:
                    return env.defined[node.value]
                elif node.value in env.builtin:
                    return env.builtin[node.value]
                else:
                    return 'Arg not defined.'

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
        print(parser.parse_block(prog))
