from analisador_lexico import tokens
import ply.yacc as yacc

endereço = 0
labels = 0
tabela = {}
resultado = ""

file = open("code2.txt", "r")

def p_prog(p):
    "prog : cod"
    global resultado
    resultado += p[1]

def p_cod_inst(p):
    "cod : cod inst ';' "
    p[0] = p[1] + p[2]

def p_cod_vazio(p):
    "cod : "
    p[0] = ""

def p_inst_print_string(p):
    "inst : PRINT '(' STRING ')' "
    p[0] = "PUSHS " + p[3] + "\n" + "WRITES\n"
    
def p_inst_print_id(p):
    "inst : PRINT '(' ID ')' "
    if p[3] not in tabela:
        print("Variable not defined")
        exit()
    
    elif tabela[p[3]][0] == "int":
        p[0] = "PUSHG " + str(tabela[p[3]][1]) + "\n" + "WRITEI\n"

    elif tabela[p[3]][0] == "string":
        p[0] = "PUSHG " + str(tabela[p[3]][1]) + "\n" + "WRITES\n"

def p_inst_print_id_array_index(p):
    "inst : PRINT '(' ID '[' INT ']' ')' "
    if p[3] not in tabela:
        print("Variable not defined")
        exit()
    
    else:
        p[0] = "PUSHG " + str(tabela[p[3]][1] + p[5]) + "\n" + "WRITEI\n"

def p_inst_print_ops(p):
    "inst : PRINT '(' ops ')' "
    
    p[0] = p[3] + "\n" + "WRITEI\n"
    
    
def p_inst_while(p):
    "inst : WHILE '(' ops ')' '{' cod '}' "
    global labels
    p[0] = "label" + str(labels) + ":\n" + p[3] + "JZ label" + str(labels + 1) + "\n" + p[6] + "JUMP " + "label" + str(labels) + "\n" + "label" + str(labels + 1) + ":\n"
    labels += 2

def p_inst_if_else(p):
    "inst : IF '(' ops ')' '{' cod '}' ELSE '{' cod '}'"
    global labels
    p[0] = p[3] + "JZ label" + str(labels) + "\n" + p[6] + "JUMP label" + str(labels+1) + "\n" + "label" + str(labels) + ":\n" + p[10] + "label" + str(labels+1) + ":\n"
    labels += 2

def p_inst_if(p):
    "inst : IF '(' ops ')' '{' cod '}' "
    global labels
    p[0] = p[3] + "JZ label" + str(labels) + "\n" + p[6] + "label" + str(labels) + ":\n"
    labels += 1
    
def p_inst_atr(p):
    "inst : expatr"
    p[0] = p[1]

def p_expatr(p):
    "expatr : atr"
    p[0] = p[1]

def p_atr_var_1d(p):
    "atr : ID '=' ops"
    if p[1] not in tabela:
        print("Variable not defined")
        exit()
    
    elif tabela[p[1]][0] != "int":
        print("Type do not match")

    else: 
        p[0] = p[3] + "STOREG " + str(tabela[p[1]][1]) + "\n"

def p_atr_var_2d(p):
    "atr : ID '[' INT ']' '=' ops"
    if p[1] not in tabela:
        print("Variable not defined")
        exit()
    
    elif p[3] > tabela[p[1]][2]:
        print("out of index") 

    elif tabela[p[1]][0] != "array_int":
        print("Type do not match")
        exit()

    else: 
        p[0] = p[6] + "STOREG " + str(tabela[p[1]][1] + p[3]) + "\n"
        

def p_atr_decl_input(p):
    "atr : TIPO_STRING ID '=' INPUT "
    global endereço
    tabela[p[2]] = ("string", endereço)

    p[0] = "READ\n"
    endereço += 1

def p_atr_input(p):
    "atr : ID '=' INPUT"
    if p[1] not in tabela:
        print("Variable not defined")
        exit()
    
    elif tabela[p[1]][0] != "string":
        print("Type do not match")
        exit()

    else:
        p[0] = "READ\n" + "STOREG " + str(tabela[p[1]][1]) + "\n"

def p_atr_ops_INT(p):
    "atr : TIPO_INT ID '=' ops"

    tabela[p[2]] = ("int", endereço - 1)

    p[0] = p[4]

def p_atr_ops_INT_vazio(p):
    "atr : TIPO_INT ID"
    global endereço
    tabela[p[2]] = ("int", endereço )
    p[0] = "PUSHI " + str('0') + "\n"
    endereço += 1 
    
def p_atr_STRING(p):
    "atr : TIPO_STRING ID '=' STRING"
    global endereço
    tabela[p[2]] = ("string", endereço)
    endereço += 1
    p[0] = "PUSHS " + p[4] + "\n"

def p_atr_STRING_Vazia(p):
    "atr : TIPO_STRING ID"
    global endereço
    tabela[p[2]] = ("string", endereço)
    endereço += 1
    p[0] = "PUSHS " + '""' + "\n"
    
def p_atr_array_vazio(p):
    "atr : TIPO_INT ID '[' INT ']' '=' '{' '}'"

    global endereço
    p[0] = "PUSHN " + str(p[4]) + "\n"

    tabela[p[2]] = ("array_int", endereço, p[4])

    endereço += p[4]

def p_atr_array_notvazio(p):
    "atr : TIPO_INT ID '[' INT ']' '=' '{' val '}'"

    p[0] = "PUSHN " + str(p[4]) + "\n" + p[8]

    tabela[p[2]] = ("array_int", endereço - p[4], p[4])

def p_val_int(p):
    "val : INT"
    global endereço
    p[0] = "PUSHI " + str(p[1]) + "\n" + "STOREG " + str(endereço) + "\n"
    endereço += 1

def p_val_vals(p):
    "val : val ',' INT"
    global endereço
    p[0] = "PUSHI " + str(p[3]) + "\n" + "STOREG " + str(endereço) + "\n" + p[1]
    endereço += 1

def p_atr_array_vazio_vazio(p):
    "atr : TIPO_INT ID '[' INT ']'"

    global endereço
    p[0] = "PUSHN " + str(p[4]) + "\n"

    tabela[p[2]] = ("array_int", endereço, p[4])

    endereço += p[4]
    
def p_ops(p):
    "ops : exl"
    p[0] = p[1]
    
def p_exl_tl(p):
    "exl : tl"
    p[0] = p[1]
    
def p_exl_or(p):
    "exl : exl OR tl"
    p[0] = p[1] + p[3] + "OR\n"
    global endereço
    endereço -= 1
    
def p_tl_fl(p):
    "tl : fl"
    p[0] = p[1]
    
def p_tl_and(p):
    "tl : tl AND fl"
    p[0] = p[1] + p[3] + "AND\n"
    global endereço
    endereço -= 1

def p_fl_rl(p):
    "fl : rl"
    p[0] = p[1]

def p_fl_not(p):
    "fl : NOT rl"
    p[0] = p[2] + "NOT\n"
    
def p_rl_exr(p):
    "rl : exr"
    p[0] = p[1]
    
def p_rl_EQUALS(p):
    "rl : rl EQUALS exr"
    p[0] = p[1] + p[3] + "EQUAL\n"
    global endereço
    endereço -= 1

def p_rl_DIFF(p):
    "rl : rl DIFF exr"
    p[0] = p[1] + p[3] + "EQUAL\nNOT\n"
    global endereço
    endereço -= 1

def p_rl_LE (p):
    "rl : rl LE exr"
    p[0] = p[1] + p[3] + "INFEQ\n"
    global endereço
    endereço -= 1
    
def p_rl_GE(p):
    "rl : rl GE exr"
    p[0] = p[1] + p[3] + "SUPEQ\n"
    global endereço
    endereço -= 1
    
def p_rl_GT(p):
    "rl : rl GT exr"
    p[0] = p[1] + p[3] + "SUP\n"
    global endereço
    endereço -= 1
    
def p_rl_LT(p):
    "rl : rl LT exr"
    p[0] = p[1] + p[3] + "INF\n"
    global endereço
    endereço -= 1

def p_exr_t(p):
    "exr : t"
    p[0] = p[1]

def p_exr_opadd(p):
    "exr : exr '+' t"
    p[0] = p[1] + p[3] + "ADD\n"
    global endereço
    endereço -= 1
    
def p_exr_opasub(p):
    "exr : exr '-' t"
    p[0] = p[1] + p[3] + "SUB\n"
    global endereço
    endereço -= 1
    
def p_t_f(p):
    "t : f"
    p[0] = p[1]

def p_t_opmmul(p):
    "t : t '*' f"
    p[0] = p[1] + p[3] + "MUL\n"
    global endereço
    endereço -= 1

def p_t_opmdiv(p):
    "t : t '/' f"
    p[0] = p[1] + p[3] + "DIV\n"
    global endereço
    endereço -= 1
    
def p_f_int(p):
    "f : INT"
    p[0] = "PUSHI " + str(p[1]) + "\n"
    global endereço
    endereço += 1

def p_f_id_array(p):
    "f : ID '[' INT ']' "
    global endereço
    endereço += 1
    if p[3] > tabela[p[1]][2]:
        print("Out of index")
        exit()

    else:   
        p[0] = "PUSHG " + str(tabela[p[1]][1] + p[3]) + "\n"

def p_f_id(p):
    "f : ID"
    global endereço
    endereço += 1
    if tabela[p[1]][0] == "int":
        p[0] = "PUSHG " + str(tabela[p[1]][1]) + "\n"
    else:
        print("Invalid operation")
        exit()

def p_f_BOOL(p):
    "f : bool"
    p[0] = p[1]

def p_bool_FALSE(p):
    "bool : FALSE"
    p[0] = "PUSHI " + str(p[1]) + "\n"
    global endereço
    endereço += 1

def p_bool_TRUE(p):
    "bool : TRUE"
    p[0] = "PUSHI " + str(p[1]) + "\n"
    global endereço
    endereço += 1

def p_f_simetrico(p):
    "f : '-' f"
    p[0] = "PUSHI " + "-1" + "\n" + str(p[2]) + "MUL\n"
    global endereço
    endereço += 1

def p_f(p):
    "f : '(' exl ')'"
    p[0] = p[2]

def p_error(p):
    parser.success = False
    print('Syntax error!!')
    exit()
    
parser = yacc.yacc()
parser.success = True

parser.parse(file.read())
file.close()

res = open("resultado.txt", "w")
res.write(resultado)
res.close()

print(resultado)
print(tabela)