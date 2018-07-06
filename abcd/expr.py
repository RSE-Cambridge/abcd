"""
command := (select <columns> | count | hist <column> | <keys>) [where <query> ]
columns := <column> [<columns>]
query := <expr> [(and | or) <query>]
expr := <id> <op> ( value | <id> )
op := gt | lt | geq | leq | eq
"""

keywords = ('COUNT', 'SELECT', 'WHERE', 'HIST_NUM', 'HIST_STR')

tokens = (
    'ID', 'NUMBER', 'REAL',
    'AND', 'OR', 'PLUS', 'MINUS',
    'LT', 'GT', 'LEQ', 'GEQ', 'EQ',
    'LPAREN', 'RPAREN',
    ) + keywords
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_LT, t_LEQ = r'<', r'<='
t_GT, t_GEQ = r'>', r'>='
t_EQ      = r'=+'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_NUMBER  = r'\d+'
t_REAL    = r'\d*\.\d*'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    try:
        t.type = {
            'where': 'WHERE',
            'count': 'COUNT',
            'hist_num': 'HIST_NUM', 'hist_str': 'HIST_STR',
            'select': 'SELECT',
            'and': 'AND', 'or': 'OR',
            'lt': 'LT', 'leq': 'LEQ',
            'gt': 'GT', 'geq': 'GEQ',
        }[t.value]
        t.value = {
            'LT': t_LT, 'LEQ': t_LEQ,
            'GT': t_GT, 'GEQ': t_GEQ,
        }[t.type]
    except KeyError:
        pass
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.linno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()


precedence = (
        ('left', 'AND', 'OR'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'LT', 'GT', 'LEQ', 'GEQ', 'EQ'),
        ('right', 'UMINUS'),
        )

def p_command_count(t):
    'command : COUNT'
    t[0] = lambda table: f'select count(*) from {table}'
def p_command_count_q(t):
    'command : COUNT WHERE expression'
    t[0] = lambda table: f'select count(*) from {table} where {t[3]}'

def p_command_select(t):
    '''command : SELECT ids
               | SELECT ids WHERE'''
    t[0] = lambda table: f'select {", ".join(t[2])} from {table}'
def p_command_select_q(t):
    'command : SELECT ids WHERE expression'
    t[0] = lambda table: f'select {", ".join(t[2])} from {table} where {t[4]}'

def p_command_hist_num(t):
    '''command : HIST_NUM ID
               | HIST_NUM ID WHERE'''
    t[0] = lambda table: f'select {t[2]} from {table}'
def p_command_hist_num_q(t):
    'command : HIST_NUM ID WHERE expression'
    t[0] = lambda table: f'select {t[2]} from {table} where {t[4]}'

def p_command_hist_str(t):
    '''command : HIST_STR ID
               | HIST_STR ID WHERE'''
    t[0] = lambda table: f'select {t[2]} as value, count(*) from {table} group by {t[2]} order by {t[2]}'
def p_command_hist_str_q(t):
    'command : HIST_STR ID WHERE expression'
    t[0] = lambda table: f'select {t[2]} as value, count(*) from {table} where {t[4]} group by {t[2]} order by {t[2]}'

def p_ids(t):
    '''ids : ID
           | ID ids'''
    r = t[2] if len(t) > 2 else []
    r.append(t[1])
    t[0] = r

def p_expression_binop(t):
    '''expression : expression AND expression
                  | expression OR expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression LT expression
                  | expression GT expression
                  | expression LEQ expression
                  | expression GEQ expression
                  | expression EQ expression'''
    t[0] = ' '.join(str(x) for x in t[1:4])

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = '-' + t[2]

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_term(t):
    '''
    expression : ID
    expression : NUMBER
    expression : REAL
    '''
    t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def parse_query(x):
    return parser.parse(x)
