import unittest
from parser.uLispParser import uLisp_parse,ParseFatalException
import pprint
from interpreter import uLispParser

simple_expression = """
    (and
      (or (> uid 1000)
          (!= gid 20)
      )
      (> quota 5.0e+03)
    )
    """

class TestSExpressionParser(unittest.TestCase):

    def test_simple_expression(self):
        s_expression = uLisp_parse.parseString(simple_expression,parseAll=True)
        self.assertEqual(3,len(s_expression[0]))

class TestULispParser(unittest.TestCase):
    def setUp(self):
        self.parser = uLispParser()

    def test_parse_simple_expression(self):
        expression = '(begin (+ 2 4))'
        parsed_expression = self.parser.parse(expression)
        self.assertEqual(['begin', ['+', 2, 4]], parsed_expression)
        self.assertEqual(2, len(parsed_expression))
        self.assertEqual(3, len(parsed_expression[1]))
