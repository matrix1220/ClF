from rply import LexerGenerator

lg = LexerGenerator()

# build up a set of token names and regexes they match 
#lg.add('FLOAT', '-?\d+.\d+')
lg.add('INTEGER', '-?\d+')
#lg.add('STRING', '(""".?""")|(".?")|(\'.?\')')
#lg.add('BOOLEAN', "true(?!\w)|false(?!\w)")
lg.add('IF', 'if(?!\w)')
lg.add('ELSE', 'else(?!\w)')
lg.add('AND', "and(?!\w)")
lg.add('OR', "or(?!\w)")
lg.add('NOT', "not(?!\w)")
#lg.add('LET', 'let(?!\w)')
#lg.add('FUNCTION', 'func(?!\w)')
#lg.add('MODULE', 'mod(?!\w)')
#lg.add('IMPORT', 'import(?!\w)')
lg.add('IDENTIFIER', "[a-zA-Z_][a-zA-Z0-9_]+")
#lg.add('COLON', ':')

lg.add('OPEN_SQUARE', '\[')
lg.add('CLOSE_SQUARE', '\]')
lg.add('OPEN_ROUND', '\(')
lg.add('CLOSE_ROUND', '\)')
lg.add('PLUS', '\+')
lg.add('ASTERISK', '\*')

lg.add('==', '==')
lg.add('!=', '!=')
lg.add('>=', '>=')
lg.add('<=', '<=')
lg.add('>', '>')
lg.add('<', '<')
lg.add('=', '=')
lg.add('{', '{')
lg.add('}', '}')
lg.add('|', '|')
lg.add(',', ',')
lg.add('.', '.')
lg.add('-', '-')

lg.add('/', '/')
lg.add('%', '%')
lg.add('NEWLINE', '\n')
 
# ignore whitespace 
lg.ignore('[ \t\r\f\v]+')

Lexer = lg.build()



from rply.token import BaseBox

class Integer(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class BinaryOparator(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOparator):
    def eval(self):
        return self.left.eval() + self.right.eval()

class Sub(BinaryOparator):
    def eval(self):
        return self.left.eval() - self.right.eval()

class Mul(BinaryOparator):
    def eval(self):
        return self.left.eval() * self.right.eval()

class Div(BinaryOparator):
    def eval(self):
        return self.left.eval() / self.right.eval()




from rply import ParserGenerator

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['INTEGER', 'IDENTIFIER', #'BOOLEAN', 
     '+', '-', '*', '/', '%', 
     'IF', 'ELSE', 'COLON', 'END', 'AND', 'OR', 'NOT',#'WHILE', 
     '(', ')', '=', '==', '!=', '>=', '<=', '<', '>', '[', ']', ',', 
     '{','}', 
     'NEWLINE', 'FUNCTION', 
 
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['+', '-']),
        ('left', ['*', '/'])
    ]
)

@pg.production('expression : INTEGER')
def expression_number(p):
    return Integer(int(p[0].getstr()))

@pg.production('expression : ( expression )')
def expression_parens(p):
    return p[1]

@pg.production('expression : expression + expression')
@pg.production('expression : expression - expression')
@pg.production('expression : expression * expression')
@pg.production('expression : expression / expression')
def expression_binop(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == '+':
        return Add(left, right)
    elif p[1].gettokentype() == '-':
        return Sub(left, right)
    elif p[1].gettokentype() == '*':
        return Mul(left, right)
    elif p[1].gettokentype() == '/':
        return Div(left, right)

@pg.production('statement : expression')
def statement_expr(state, p):
    return p[0]


Parser = pg.build()

print(Parser.parse(Lexer.lex('1 + 2*5')).eval())