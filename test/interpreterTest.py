import unittest
from interpreter import *


class TestULispInterpreter(unittest.TestCase):
    def setUp(self):
        self.evaluator = SyntacticEvaluator()
        self.global_env = add_globals(Environment())
        self.parser = uLispParser()

    def test_boolean_expression(self):
        self.assertEqual(False, self.evaluator.evaluate(self.parser.parse("(equal 5 3)")), self.global_env)

    def testLispResult(self):
        #mejorar el parser y el interprete para que se pueda bancar la definicion de un defun con parametros
        self.assertEqual(50, self.evaluator.evaluate(
            self.parser.parse("(begin (defun add (lambda (num1 num2) (+ num1 num2))) (add 44 6))")), self.global_env)


class TestULispParser(unittest.TestCase):
    def setUp(self):
        self.parser = uLispParser()

    def test_parse_simple_expression(self):
        expression = '(begin (+ 2 4))'
        parsed_expression = self.parser.parse(expression)
        self.assertEqual(['begin', ['+', 2, 4]], parsed_expression)
        self.assertEqual(2, len(parsed_expression))
        self.assertEqual(3, len(parsed_expression[1]))
        print(self.parser.parse(expression))

    def test_parse_new_parser(self):
        expression = "(begin (defun add (lambda (num1 num2) (+ num1 num2))) (add 44 6))"
        print(self.parser.parse(expression))


class TestSyntaticExpression(unittest.TestCase):
    def setUp(self):
        self.test_function_name = 'function_test'

    def function_test(self):
        pass

    def test_change_function(self):
        change_function(self, self.test_function_name, 'return 42')
        self.assertEqual(42, self.function_test())

    def test_change_multilinefunction(self):
        change_function(self, self.test_function_name, 'var=1\n    return var+1')
        self.assertEqual(2, self.function_test())

    def test_syntatic_condition_creation(self):
        pass