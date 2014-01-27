from unittest import TestCase
from uLisp.parser.uLispParser import uLisp_parse

simple_expression = """
    (and
      (or (> uid 1000)
          (!= gid 20)
      )
      (> quota 5.0e+03)
    )
    """
simple_lambda = """(lambda (x) (* x x))"""
complex_lambda = """(def length
   (lambda (x)
      (cond
         ((not x) 0)
         (   t   (+ 1 (length (cdr x))))
      )
   )
)
"""

class ParserTest(TestCase):
    def setUp(self):
        self.parser = uLisp_parse

    def test_parse_simple_expression(self):
        parsed = self.parser.parseString(simple_expression, parseAll=True)
        self.assertEqual(3, len(parsed[0]))
        self.assertEqual('and', parsed[0][0])
        self.assertEqual('or', parsed[0][1][0])
        self.assertEqual('>', parsed[0][1][1][0])
        self.assertEqual(3, len(parsed[0][2]))

    def test_simple_lambda(self):
        parsed = self.parser.parseString(simple_lambda, parseAll=True)
        self.assertEqual(3, len(parsed[0]))
        self.assertEqual('lambda', parsed[0][0])
        self.assertEqual((['*', 'x', 'x'], {}), parsed[0][2])

    def test_complex_lambda(self):
        parsed = self.parser.parseString(complex_lambda, parseAll=True)
        self.assertEqual(3, len(parsed[0]))
        self.assertEqual(3, len(parsed[0][2]))


