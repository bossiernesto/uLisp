from utils import change_function
from parser.parserWrapper import uLispParser

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
    This a common interface to define syntatic expressions
    """

    def check_condition(self, expression, env=global_env):
        raise NotImplementedError

    def do_action(self, expression, env):
        raise NotImplementedError


class DynamicSyntacticExpression(SyntacticExpression):
    """
    This a common interface to define syntatic expressions, that can be set on runtime
    """

    def __init__(self, condition, action):
        super().__init__()
        change_function(self, 'check_condition', condition)
        change_function(self, 'do_action', action)

    def check_condition(self, expression, env=global_env):
        pass

    def do_action(self, expression, env):
        pass


global_eval_conditions = [
    ('isinstance(expression, Symbol)', 'return env.find(expression)[expression]'),
    ('not isinstance(expression, list)', 'return expression'),
    ('expression[0] == "quote"', '(_, exp) = expression\n    return exp'),
    ('expression[0] == "if"',
     '(_, test, conseq, alt) = expression\n    return eval((conseq if eval(test, env) else alt), env)'),
    ('expression[0] == "setq"', '(_, var, exp) = expression\n    env.find(var)[var] = eval(exp, env))'),
    ('expression[0] == "defun"', '(_, var, exp) = expression\n    env[var] = eval(exp, env))'),
    ('expression[0] == "lambda"',
     '(_, vars, exp) = expression\n    return lambda *args: eval(exp, Environment(vars, args, en'),
    ('expression[0] == "begin"', 'for exp in expression[1:]:\n        val = eval(exp, env)\n    return val')
]


class SyntacticEvaluator(object):
    def __init__(self, initial_evaluator=global_eval_conditions):
        self.expressions = []
        for condition in global_eval_conditions:
            self.add_syntatic_expression(condition)

    def add_syntatic_expression(self, expression_tuple):
        self.expressions.append(SyntacticExpression(*expression_tuple))

    def evaluate(self, expression, env=global_env):
        for expr in self.expressions:
            if expr.check_condition(expression, env):
                return expr.do_action(expression, env)
                # (proc exp*)
        exps = [self.eval(exp, env) for exp in expression]
        proc = exps.pop(0)
        return proc(*exps)


class Interpreter(object):
    def __init__(self, environment=None):
        self.environment = environment or Environment()
        self.parser = uLispParser()
        self.evaluator = SyntacticEvaluator()

    #Repl should admit not only a file type but also a IOBuffer or string
    def repl(self, prompt='lis.py> '):
        "A prompt-read-eval-print loop."
        if isinstance(prompt, str):
            self.repl_sentence(prompt)
        else:
            while True:
                self.repl_sentence(input(prompt))

    def repl_sentence(self, sentence):
        val = self.evaluator.evaluate(self.parser.parse(sentence))
        if val is not None:
            print(self.parser.to_string(val))

