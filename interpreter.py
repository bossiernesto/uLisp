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

class Interpreter(object):
    def __init__(self, environment=None):
        from syntaticEvaluator.syntaticEvaluator import SyntacticEvaluator
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

