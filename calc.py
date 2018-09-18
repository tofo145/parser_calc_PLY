from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys

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
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def p_statement_expr(p):
        '''statement  : expr_cont
           expression : atom
           expr_cont  : atom'''
        p[0] = p[1]

    def p_expression_add(p):
        '''expression : expression '+' expression
           expr_cont  : expr_cont  '+' expression'''
        try:
            p[0] = p[1] + p[3]
        except TypeError:
            print('Error. Previous result not found.')
            
    def p_expression_sub(p):
        '''expression : expression '-' expression
           expr_cont  :  expr_cont '-' expression'''
        try:
            p[0] = p[1] - p[3]
        except TypeError:
            print('Error. Previous result not found.')
                  
    def p_expression_mul(p):
        '''expression : expression '*' expression
           expr_cont  :  expr_cont '*' expression'''
        try:
            p[0] = p[1] * p[3]
        except TypeError:
            print('Error. Previous result not found.')
                  
    def p_expression_div(p):
        '''expression : expression '/' expression
           expr_cont  :  expr_cont '/' expression'''
        try:
            p[0] = p[1] / p[3]
        except ZeroDivisionError:
            print('Cannot divide by zero')
        except TypeError:
            print('Error. Previous result not found.')
        
    def p_atom_uminus(p):
        "atom : '-' atom %prec UMINUS"
        p[0] = -p[2]
        
    def p_atom_group(p):
        "atom : '(' expression ')'"
        p[0] = p[2]

    def p_expr_previous(p):
        "expr_cont : "
        p[0] = r
    
    def p_expression_number(p):
        "atom : NUMBER"
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
            line.rstrip('\n')
            r = calc(line)
            print("{0} = {1}".format(line, r))
    else:
        r = calc(s)
        print(r)
