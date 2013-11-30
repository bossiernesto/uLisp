import unittest
from interpreter import *
from syntaticEvaluator.syntaticEvaluator import SyntacticEvaluator


class TestULispInterpreter(unittest.TestCase):
    def setUp(self):
        self.evaluator = SyntacticEvaluator()
        self.global_env = add_globals(Environment())
        self.parser = uLispParser()

    def test_boolean_expression(self):
        self.assertEqual(False, self.evaluator.evaluate(self.parser.parse("(equal 5 3)")), self.global_env)

    def test_lisp_result(self):
        #mejorar el parser y el interprete para que se pueda bancar la definicion de un defun con parametros
        self.assertEqual(50, self.evaluator.evaluate(
            self.parser.parse("(begin (defun add (lambda (num1 num2) (+ num1 num2))) (add 44 6))")), self.global_env)

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


class TestULispParser(unittest.TestCase):
    def setUp(self):
        self.parser = uLispParser()

    def test_parse_simple_expression(self):
        expression = '(begin (+ 2 4))'
        parsed_expression = self.parser.parse(expression)
        self.assertEqual(['begin', ['+', 2, 4]], parsed_expression)
        self.assertEqual(2, len(parsed_expression))
        self.assertEqual(3, len(parsed_expression[1]))


