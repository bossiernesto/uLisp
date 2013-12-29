import unittest
from parser.uLispParser import uLisp_parse,ParseFatalException
import pprint

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
        pprint.pprint(s_expression.asList())
