from unittest import TestCase,skip
from uLisp.interpreter import *
from uLisp.syntaticEvaluator.syntaticEvaluator import SyntacticEvaluator

class TestLispInterpreter(TestCase):

    def setUp(self):
        self.evaluator = SyntacticEvaluator()
        self.parser = uLispParser()
        self.interpreter= Interpreter()

    @skip
    def test_bleh(self):
        parsed = self.parser.parse("(begin 2)")
        self.assertEqual(2,self.evaluator.evaluate(parsed))

    def test_interpret_fst(self):
        parsed=self.parser.parse(("(begin "
                                  "(car (list 3 2 6 8))"
                                  ")"))
        self.assertEqual(3,self.evaluator.evaluate(parsed))

    @skip
    def test_interpreter(self):
        self.interpreter.repl("(* 1 2)")
