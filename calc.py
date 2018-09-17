from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

# Make a calculator function

def make_calculator():
    import ply.lex as lex
    import ply.yacc as yacc
    
    # Tokenizing rules

    tokens = (
        'NUMBER',
    )

    literals = ['=', '+', '-', '*', '/', '(', ')']

    t_ignore = " \t"

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    lexer = lex.lex()

    # Parsing rules
    precedence = (
        ('left', '+', '-'),
        ('right', 'MORADD', 'MORSUB'),
        ('left', '*', '/'),
        ('right', 'MORMUL', 'MORDIV'),
        ('right', 'UMINUS'),
    )

    def p_statement_expr(p):
        'statement : expression'
        p[0] = p[1]
        print('Calculation complete')

    def p_expression_binop(p):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression'''
        if p[2] == '+':
            p[0] = p[1] + p[3]
            print('Addition ', p[0])
        elif p[2] == '-':
            p[0] = p[1] - p[3]
            print('Subtraction ', p[0])
        elif p[2] == '*':
            p[0] = p[1] * p[3]
            print('Multiplication ', p[0])
        elif p[2] == '/':
            p[0] = p[1] / p[3]
            print('Division ', p[0])

    # Executed after binop, so results can often be wrong when continuing
    # calculations on a previous result and an expression starts with '*' or '/'
    # Ex.: Previous result was 9. When executing '*2+2' the result should be 20,
    # but since the binop is performed first, it returns 36
    def p_expression_more(p):
        '''expression : '+' expression %prec MORADD
                      | '-' expression %prec MORSUB
                      | '*' expression %prec MORMUL
                      | '/' expression %prec MORDIV '''
        if p[1] == '+':
            p[0] = r + p[2]
            print('Addition2 ', p[0])
        elif p[1] == '-':
            p[0] = r - p[2]
            print('Subtraction2 ', p[0])
        elif p[1] == '*':
            p[0] = r * p[2]
            print('Multiplication2 ', p[0])
        elif p[1] == '/':
            p[0] = r / p[2]
            print('Division2 ', p[0])    

    # Reduce/Reduce conflict with above '-' statement
    # Solved Reduce/Reduce conflict by requiring parentheses
    def p_expression_uminus(p):
        "expression : '(' '-' expression ')' %prec UMINUS"
        p[0] = -p[3]
        print('Doing the thing')
        
    def p_expression_group(p):
        "expression : '(' expression ')'"
        p[0] = p[2]
        print('Parentheses!')

    def p_expression_number(p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_error(p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

    # Build the parser
    parser = yacc.yacc()

    # Input function

    def input(text):
        result = parser.parse(text, lexer=lexer)
        return result

    return input

# Make a calculator object and use it
calc = make_calculator()
print('Type a calculation and execute with ENTER. Type \'open\' to choose a file to do calculations from.')
r = 0 # Initiate so calculator doesn't crash if -(-'X') is first input

while True:
    try:
        s = raw_input("calc > ")
    except EOFError:
        break

    # Open a file and calculate each line
    if s == 'open':
        print('Choose file')
        Tk().withdraw()
        filename = askopenfilename()
        print(filename)
        with open(filename) as f:
            file = f.readlines()
        for line in file:
            r = calc(line)
            print(r)
    else:
        r = calc(s)
        print(r)
