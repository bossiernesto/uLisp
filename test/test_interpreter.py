import unittest
from unittest import skip
from uLisp.interpreter import *
from uLisp.syntaticEvaluator.syntaticEvaluator import SyntacticEvaluator

class TestULispInterpreter(unittest.TestCase):
    def setUp(self):
        self.evaluator = SyntacticEvaluator()
        self.global_env = add_globals(Environment())
        self.parser = uLispParser()

    def test_boolean_expression(self):
        self.assertEqual(False, self.evaluator.evaluate(self.parser.parse("(equal 5 3)")), self.global_env)

    @skip
    def test_lisp_result(self):
        #mejorar el parser y el interprete para que se pueda bancar la definicion de un defun con parametros sin tener llamarlo por un lambda
        parsed = self.parser.parse("(begin "
                              "(foo 44 6)"
                              "(defun foo (lambda (num1 num2) (+ num1 num2)))"
                              ")")
        self.assertEqual(50, self.evaluator.evaluate(parsed), self.global_env)

    def test_interpret_fst(self):
        parsed=self.parser.parse(('(begin '
                                  '(car (list 3 2))'
                                  ')'))
        self.assertEqual(3,self.evaluator.evaluate(parsed))

    def test_simple_interpretation(self):
        self.assertEqual(1, self.evaluator.evaluate(self.parser.parse("(begin 1)")))

    def test_if_and_recursive_interpretation(self):
        parsed = self.parser.parse("(begin   (defun factorial (lambda (x)"
                                   "(if (= x 0) 1"
                                   "(* x (factorial (- x 1)))"
                                   ")"
                                   ")) (factorial 5))")
        self.assertEqual(120, self.evaluator.evaluate(parsed))

    def test_invalid_interpretation(self):
        parsed = self.parser.parse("(begin (1 2))")
        self.assertRaises(TypeError, self.evaluator.evaluate, parsed)

    def test_(self):
        #4 == (2 + 2)
        parsed = self.parser.parse("(begin (equal 4 (+ 2 2)))")
        self.assertEqual(True, self.evaluator.evaluate(parsed))
