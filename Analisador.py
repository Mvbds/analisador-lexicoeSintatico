import ply.lex as lex
import ply.yacc as yacc

# Definição dos tokens
tokens = (
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'GT', 'SEMICOLON'
)

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'int': 'INT',
    'float': 'FLOAT'
}

tokens += tuple(reserved.values())

# Regras para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_GT = r'>'
t_SEMICOLON = r';'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica palavras reservadas
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Definição da gramática
start = 'program'  # Define a regra de início da gramática

def p_program(p):
    '''program : statement
               | statement program'''
    pass

def p_statement(p):
    '''statement : declaracao
                 | expressao
                 | condicional'''
    pass

def p_declaracao_variavel(p):
    'declaracao : INT ID EQUALS NUMBER SEMICOLON'
    print(f"Declaração de variável: {p[2]} = {p[4]}")

def p_expressao(p):
    '''expressao : ID EQUALS ID PLUS NUMBER SEMICOLON
                 | ID EQUALS ID MINUS NUMBER SEMICOLON
                 | ID EQUALS ID TIMES NUMBER SEMICOLON
                 | ID EQUALS ID DIVIDE NUMBER SEMICOLON'''
    print(f"Expressão: {p[1]} = {p[3]} {p[4]} {p[5]}")


def p_condicional(p):
    'condicional : IF LPAREN ID GT NUMBER RPAREN LBRACE RBRACE'
    print(f"Condição: if ({p[3]} > {p[5]})")

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo a '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do código")

parser = yacc.yacc()

# Testando o analisador
codigo = """
int x = 10;
y = x + 2;
if (x > 0) { }
"""

print("\n=== Analisador Léxico ===")
lexer.input(codigo)
for token in lexer:
    print(token)

print("\n=== Analisador Sintático ===")
parser.parse(codigo, lexer=lexer)
