import ply.lex as lex

literals = [',','(',')','[',']','{','}',';','=','+','-','*','/']

tokens = ('ID','TIPO_INT','TIPO_STRING','NOT','AND','OR','TRUE','FALSE','INT','IF','ELSE','WHILE','INPUT','PRINT','STRING', 'GE', 'GT', 'LT', 'LE', 'EQUALS', 'DIFF')

t_EQUALS = r'=='

t_DIFF = r'!='

t_LE = r'<='

t_GE = r'>='

t_GT = r'>'

t_LT = r'<'

t_ID = r'[a-zA-Z]+'

def t_TIPO_STRING(t):
    r'string'
    return t

def t_TIPO_INT(t):
    r'int'
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    return t
    
def t_PRINT(t):
    r'print'
    return t

def t_INPUT(t):
    r'input'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_IF(t):
     r'if'
     return t

def t_OR(t):
    r'or'
    return t

def t_AND(t):
    r'and'
    return t

def t_NOT(t):
    r'not'
    return t

def t_TRUE(t):
    r'True'
    t.value = 1
    return t

def t_FALSE(t):
    r'False'
    t.value = 0
    return t

def t_INT(t):
    r'(\d+)'
    t.value = int(t.value) 
    return t

t_ignore = ' \r\n\t'

def t_error(t):
    print('Illegal character: ' + t.value[0])
    return

lexer = lex.lex() # cria um AnaLex especifico a partir da especificação acima usando o gerador 'lex' do objeto 'lex'

# Reading input
#f = input(">> ")
#lexer.input(f) 
#simb = lexer.token()
#while simb:
#    print(simb)
#    simb = lexer.token()