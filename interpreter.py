from utils import change_function

Symbol = str

#this will have to be changed to support a multiple NameSpace as CL does.
#Enviroment should define a merge/join of another Enviroment, like when loading a library, or an snapshoted state(?)
# meoize the Enviroment
#Give the user two type of different Enviroments one with it's globals inmuttable and the other without this restriction
class Environment(dict):
    """An environment: a dict of {'var':val} pairs"""

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears."""
        return self if var in self else self.outer.find(var)


def add_globals(env):
    """Add some CommonLisp standard procedures to an environment."""
    import math
    import operator as op

    env.update(vars(math)) # sin, sqrt, ...
    env.update(
        {'+': op.add,
         '-': op.sub,
         '*': op.mul,
         '/': op.truediv,
         'not': op.not_,
         '>': op.gt,
         '<': op.lt,
         '>=': op.ge,
         '<=': op.le,
         '=': op.eq,
         'equal': op.eq,
         'eq': op.is_,
         'length': len,
         'cons': lambda x, y: [x] + y,
         'car': lambda x: x[0],
         'cdr': lambda x: x[1:],
         'append': op.add,
         'list': lambda *x: list(x),
         'list?': lambda x: isinstance(x, list),
         'null?': lambda x: x == [],
         'symbol?': lambda x: isinstance(x, Symbol)})
    return env


global_env = add_globals(Environment())


class SyntacticExpression(object):
    """
    This a common interface to define syntatic expressions, that can be set on runtime
    """

    def __init__(self, condition, action):
        change_function(self, 'check_condition', condition)
        change_function(self, 'do_action', action)

    def check_condition(self, expression, env=global_env):
        raise NotImplemented

    def do_action(self, expression, env):
        raise NotImplemented


global_eval_conditions = [
    ('isinstance(expression, Symbol)', 'return env.find(expression)[expression]'),
    ('not isinstance(expression, list)', 'return expression'),
    ('expression[0] == "quote"', '(_, exp) = expression\n\treturn exp'),
    ('expression[0] == "if"',
     '(_, test, conseq, alt) = expression\n\treturn eval((conseq if eval(test, env) else alt), env)'),
    ('expression[0] == "setq"', '(_, var, exp) = expression\n\tenv.find(var)[var] = eval(exp, env))'),
    ('expression[0] == "defun"', '(_, var, exp) = expression\n\tenv[var] = eval(exp, env))'),
    ('expression[0] == "lambda"',
     '(_, vars, exp) = expression\n\treturn lambda *args: eval(exp, Environment(vars, args, en'),
    ('expression[0] == "begin"', 'for exp in expression[1:]:\n\t\tval = eval(exp, env)\n\treturn val')
]


class SyntacticEvaluator(object):
    def __init__(self, initial_evaluator=global_eval_conditions):
        self.expressions = []
        for condition in global_eval_conditions:
            self.add_syntatic_expression(condition)

    def add_syntatic_expression(self, expression_tuple):
        self.expressions.append(SyntacticExpression(*expression_tuple))

    def eval(self, expression, env=global_env):
        for expr in self.expressions:
            if expr.check_condition(expression, env):
                return expr.do_action(expression, env)
                # (proc exp*)
        exps = [self.eval(exp, env) for exp in expression]
        proc = exps.pop(0)
        return proc(*exps)

#old version delete after testing new one :P
def evaluate(expression, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(expression, Symbol):             # variable reference
        return env.find(expression)[expression]
    elif not isinstance(expression, list):         # constant literal
        return expression
    elif expression[0] == 'quote':          # (quote exp)
        (_, exp) = expression
        return exp
    elif expression[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = expression
        return evaluate((conseq if evaluate(test, env) else alt), env)
    elif expression[0] == 'setq':           # (set! var exp)
        (_, var, exp) = expression
        env.find(var)[var] = evaluate(exp, env)
    elif expression[0] == 'defun':         # (define var exp)
        (_, var, exp) = expression
        env[var] = evaluate(exp, env)
    elif expression[0] == 'lambda':         # (lambda (var*) exp)
        (_, vars, exp) = expression
        return lambda *args: evaluate(exp, Environment(vars, args, env))
    elif expression[0] == 'begin':          # (begin exp*)
        for exp in expression[1:]:
            val = evaluate(exp, env)
        return val
    else:                          # (proc exp*)
        exps = [evaluate(exp, env) for exp in expression]
        proc = exps.pop(0)
        return proc(*exps)


class uLispParser(object):
    def parse(self, string):
        from uLispParser import uLisp_parse

        return uLisp_parse.parseString(string).asList()[0]

    def to_table(self, lisp_expression):
        from texttable import Texttable

        tab = Texttable()
        for row in lisp_expression:
            row = dict(row)
            tab.header(row.keys())
            tab.add_row(row.values())
        print(tab.draw())

    def to_string(self, lisp_expression):
        return '(%s)' % ' '.join(self.to_string(y) for y in lisp_expression) if isinstance(lisp_expression,
                                                                                           list) else lisp_expression


class Interpreter(object):
    def __init__(self, environment=None):
        self.environment = environment or Environment()
        self.parser = uLispParser()

    #Repl should admit not only a file type but also a IOBuffer or string
    def repl(self, prompt='lis.py> '):
        "A prompt-read-eval-print loop."
        if isinstance(prompt, str):
            self.repl_sentence(prompt)
        else:
            while True:
                self.repl_sentence(input(prompt))


    def repl_sentence(self, sentence):
        val = evaluate(self.parser.parse(sentence))
        if val is not None:
            print(self.parser.to_string(val))

