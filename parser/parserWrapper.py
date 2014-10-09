class uLispParser(object):

    def parse(self, string):
        from parser.uLispParser import uLisp_parse
        return uLisp_parse.parseString(string).asList()[0]

    def to_table(self, lisp_expression):
        from texttable import Texttable #hay que migrar Texttable a python 3 :/

        tab = Texttable()
        for row in lisp_expression:
            row = dict(row)
            tab.header(row.keys())
            tab.add_row(row.values())
        print(tab.draw())

    def to_string(self, lisp_expression):
        return '(%s)' % ' '.join(self.to_string(y) for y in lisp_expression) if isinstance(lisp_expression,
                                                                                           list) else lisp_expression
