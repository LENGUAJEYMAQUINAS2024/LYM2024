#Trabajo lenguaje y maquinas
#proyecto 0
#Samuel Osorio 202324806 Alejandro Salcedo 202321921

tokens_textuales = ["EXEC", "NEW","J","G", "VAR"
                    "MACRO","TURNTOMY","TURNTOTHE", "WALK", "JUMP","DROP","PICK","GRAB",
                    "LETGO","POP","MOVES","NOP","SAFEEXE","IF","DO","NOT"
                    
]


Tokens_symbol_struct = ["(",",",")",":","=",";","{","}","THEN","ELSE","TIMES","REPEAT","FI","OD"]

Constantes = ["SIZE", "MYX","MYY", "MYCHIPS", "MYBALLONS", "BALLONSHERE", "CHIPSHERE","ROOMFORCHIPS"]

condiciones=["ISBLOCKED?","ISFACING?","ZERO?"]



input_file="code-examplesOK (1).txt"

def lexer(input_file):
    tokens_final=[]
    with open(input_file, "r") as file:
        text = file.read()
    key_words=[]
    actual=""
    
    for char in text:
        if char=="?" or char.isalnum():  
            actual += char
        elif char in Tokens_symbol_struct: 
            if actual:  
                key_words.append(actual)
                actual=""  
            key_words.append(char)  
        elif char.isspace():  
            if actual:  
                key_words.append(actual)  
                actual=""
    i=0
    palabra=None
    while i < len(key_words):  
        palabra=key_words[i].upper()
        tokens_final.append(palabra)
        i+=1
    return tokens_final

def inicio(lista_final):
    if lista_final[0]!="EXEC" or lista_final[len(lista_final)-1] != "}":
        return False
    return True

def variable(palabra):
    if palabra not in Tokens_symbol_struct and palabra not in tokens_textuales and palabra not in Constantes and palabra not in condiciones:
        return True
    return False
#para el comando moves
def validar_moves(lista_final, posicion):
    if lista_final[posicion+1]== "(" and lista_final[posicion+2] in MOVES:
        posicion+=2  
        contador=2
        while posicion + 1 < len(lista_final):
            posicion += 1  
            c = lista_final[posicion]
            
            
            if c == ")":
                contador+=1
                return True,contador
            
           
            elif c == ",":
                
                if posicion + 1 < len(lista_final) and lista_final[posicion+1] in MOVES:
                    posicion += 1 
                    contador+=1
                else:
                    return False,contador
            
            else:
                return False, contador
    
    return False, contador


funcion_valor=["WALK","JUMP","DROP","PICK","GRAB","LETGO","POP"]
DIRECCIONES=["LEFT","RIGHT","BACK"]
MOVES=["BACK","FRONT","BACKWARDS","FORWARD"]
#los comandos
def tokens_pri(lista_final, posicion):
    i=0
    token=lista_final[posicion]
    if token == "TURNTOMY":
        if lista_final[posicion+1]=="(":
            if lista_final[posicion+2] in DIRECCIONES:
                if lista_final[posicion+3]==")" and lista_final[posicion+4]==";":
                    i=4
                    return True, i
    elif token== "TURNTOTHE":
        if lista_final[posicion+1]=="(":
            if lista_final[posicion+2] in FACING:
                if lista_final[posicion+3]==")" and lista_final[posicion+4]==";":
                    i=4
                    return True, i
    elif token in funcion_valor:
        if lista_final[posicion+1]=="(":
            if variable(lista_final[posicion+2]) or lista_final[posicion+2].isdigit(): 
                if lista_final[posicion+3]==")" and lista_final[posicion+4]==";":
                    i=4
                    return True, i
    elif token =="MOVES":
        if validar_moves(lista_final,posicion)[0]:
            i=validar_moves[1]
            return True, i
    elif token == "NOP":
        if lista_final[posicion+1]==";":
            i=1
            return True, i
    elif token== "SAFEEXE":
        if lista_final[posicion+1]=="(":
            if lista_final[posicion+2] in funcion_valor:
                if lista_final[posicion+3]=="(":
                    if variable(lista_final[posicion+4]) or lista_final[posicion+4].isdigit():
                        if lista_final[posicion+5]==")" and lista_final[posicion+6]==";":
                            i=6
                            return True, i
    elif token== "G":
        if lista_final[posicion+1]=="(":
            if variable(lista_final[posicion+2]) or lista_final[posicion+2].isdigit():
                if lista_final[posicion+3]==",":
                    if variable(lista_final[posicion+4]) or lista_final[posicion+4].isdigit() and lista_final[posicion+5]==")":
                        i=5
                        return True,i
    elif token== "J":
        if lista_final[posicion+1]=="(":
            if variable(lista_final[posicion+2]) or lista_final[posicion+2].isdigit():
                if lista_final[posicion+3]==")":
                    i=3
                    return True, i
        
    return False, i
                        
                    
BLOCKED=["LEFT","RIGHT","FRONT","BACK"]
FACING=["NORTH","SOUTH","WEST","EAST"]
excepciones=["EXEC","NEW","VAR","THEN"]

def IF(lista_final,posicion):
    i=0
    if lista_final[posicion+2]=="NOT":
        if lista_final[posicion+3] =="(" and lista_final[posicion+4] in condiciones:
            if lista_final[posicion+5]=="(" :
                if lista_final[posicion+4]=="ISBLOCKED?" and lista_final[posicion+6] in BLOCKED:
                    if lista_final[posicion+7]==")" and lista_final[posicion+8]==")" and lista_final[posicion+9]==")":
                        i=9
                        return True, i
                elif lista_final[posicion+4]=="ISFACING?" and lista_final[posicion+6] in FACING:
                    if lista_final[posicion+7]==")" and lista_final[posicion+8]==")" and lista_final[posicion+9]==")":
                        i=9
                        return True, i
                elif lista_final[posicion+4]=="ZERO?" and lista_final[posicion+6] in Constantes:
                    if lista_final[posicion+7]==")" and lista_final[posicion+8]==")" and lista_final[posicion+9]==")":
                        i=9
                        return True, i
                    
    elif lista_final[posicion+2] in condiciones:
        if lista_final[posicion+3]=="(":
            if lista_final[posicion+2]=="ISBLOCKED?" and lista_final[posicion+4] in BLOCKED:
                 if lista_final[posicion+5]==")" and lista_final[posicion+6]==")":
                     i=6
                     return True, i
            elif lista_final[posicion+2]=="ISFACING?" and lista_final[posicion+4] in FACING:
                if lista_final[posicion+5]==")" and lista_final[posicion+6]==")":
                    i=6
                    return True, i
            elif lista_final[posicion+2]=="ZERO?" and lista_final[posicion+4] in Constantes:
                if lista_final[posicion+5]==")" and lista_final[posicion+6]==")":
                    i=6
                    return True, i
    return False, 0

def DO(lista_final,posicion):
    i=0
    if lista_final[posicion+2]=="NOT":
        if lista_final[posicion+3] =="(" and lista_final[posicion+4] in condiciones:
            if lista_final[posicion+5]=="(" :
                if lista_final[posicion+4]=="ISBLOCKED?" and lista_final[posicion+6] in BLOCKED:
                    if lista_final[posicion+7]==")" and lista_final[posicion+8]==")" and lista_final[posicion+9]==")":
                        i=9
                        return True, i
                elif lista_final[posicion+4]=="ISFACING?" and lista_final[posicion+6] in FACING:
                    if lista_final[posicion+7]==")" and lista_final[posicion+8]==")" and lista_final[posicion+9]==")":
                        i=9
                        return True, i
                elif lista_final[posicion+4]=="ZERO?" and lista_final[posicion+6] in Constantes:
                    if lista_final[posicion+7]==")" and lista_final[posicion+8]==")" and lista_final[posicion+9]==")":
                        i=9
                        return True, i
    elif lista_final[posicion+2] in condiciones:
        if lista_final[posicion+3]=="(":
            if lista_final[posicion+2]=="ISBLOCKED?" and lista_final[posicion+4] in BLOCKED:
                 if lista_final[posicion+5]==")" and lista_final[posicion+6]==")":
                     i=6
                     return True, i
            elif lista_final[posicion+2]=="ISFACING?" and lista_final[posicion+4] in FACING:
                if lista_final[posicion+5]==")" and lista_final[posicion+6]==")":
                    i=6
                    return True, i
            elif lista_final[posicion+2]=="ZERO?" and lista_final[posicion+4] in Constantes:
                if lista_final[posicion+5]==")" and lista_final[posicion+6]==")":
                    i=6
                    return True, i
    return False, 0
    

COMANDS=["TURNTOMY","TURNTOTHE", "WALK", "JUMP","DROP","PICK","GRAB",
                    "LETGO","POP","MOVES","NOP","SAFEEXE","IF","DO","NOT","J","G"]

def THEN(lista_final,posicion):
    #posicion=then
    i=0
    if lista_final[posicion+2] in COMANDS:
        if tokens_pri(lista_final,i+2)[0]:
            i+=2
            i+=tokens_pri(lista_final,i+2)[1]
            if lista_final[posicion+i+1]=="}":
                i+=1
                return True, i
            elif variable(lista_final[posicion+i+1]) and lista_final[posicion+i+2]=="(" and lista_final[posicion+i+3]:
                i+=3
                return True, i
    return False, i

def ELSE(lista_final,posicion):
    i=0
    if lista_final[posicion+1]=="{":
        if tokens_pri(lista_final,posicion+2)[0]:
            i+=tokens_pri(lista_final,posicion+2)[1]
            if lista_final[posicion+2+i+1]=="}":
                i+=3
                return True,i
    return False,i
    
                
    
def parser(lista_final):
    r=True
    i=0
    while i < len(lista_final):
        if i==0 and inicio(lista_final):
            i+=1
            
            
        #para exec
        elif lista_final[i]=="EXEC":
            if i+1 < len(lista_final) and lista_final[i+1]== "{":
                i+=1
            else:
                r=False
                break
        #para new
        elif lista_final[i]=="NEW":
            if i+1 < len(lista_final):
                if lista_final[i+1]=="VAR" or lista_final[i+1]=="MACRO":
                    i+=1
                else:
                    r=False
                    break
            else:
                r=False 
                break
            
        #para var y macro
        elif lista_final[i]=="VAR" or lista_final[i]=="MACRO":
            if i+1 < len(lista_final):
                if lista_final[i-1]=="NEW" and variable(lista_final[i+1]):
                    i+=1
                else:
                    r=False
                    break
            else:
                r=False 
                break
        #para variables
        elif variable(lista_final[i]):
            if lista_final[i-1]=="VAR" and i+1 < len(lista_final):
                if lista_final[i+1]=="=":
                    i+=1
                else:
                    r=False
                    break
            elif lista_final[i-1]=="MACRO" and i+1 < len(lista_final):
                if lista_final[i+1]=="(":
                    i+=1
                else:
                    r=False
                    break
            else:
                r=False
                break
            
        #tokens
        elif lista_final[i] in tokens_textuales:
            if lista_final[i]=="IF" and lista_final[i+1]=="(" and lista_final[i-1]=="{":
                if IF(lista_final,i)[0]:
                    i+=IF(lista_final,i)[1]
                    i+=1
                    #puede ser then o {}
                    if lista_final[i]=="THEN" and lista_final[i+1]=="{":
                        if THEN(lista_final,i)[0]:
                            i+=THEN(lista_final,i)[1]
                            i+=1
                            if lista_final[i]=="ELSE":
                                if ELSE(lista_final,i)[0]:
                                    i+=ELSE(lista_final,i)[1]
                                    i+=1
                                    if lista_final[i]=="FI" and lista_final[i+1]==";" and lista_final[i+2]=="}":
                                        i+=3
                                    else:
                                        r=False
                                        break
                                else:
                                    r=False
                                    break
                            else:
                                r=False
                                break  
                        else:
                            r=False 
                            break
                    elif lista_final[i]=="{" and tokens_pri(lista_final,i+1)[0]:
                        
                        i+=tokens_pri(lista_final,i+1)[1]
                        i+=1
                        if lista_final[i+1]=="}":
                            i+=1
                        else:
                            r=False
                            break
                    else:
                        r=False
                        break      
                else:
                    r=False
                    break
            elif lista_final[i]=="DO" and lista_final[i+1]=="(" and lista_final[i-1]=="{":
                if DO(lista_final,i)[0]:
                    i+= DO(lista_final,i)[1]
                    i+=1
                    p=i
                        
                else:
                    r=False
                    break
            elif tokens_pri(lista_final,i):
                i+=1
            else:
                r=False
                break
        #;
        elif lista_final[i]==";" :
            if lista_final[i+1]=="}":
                i+=1
            else:
                r=False
                break
        #}
        elif lista_final[i]=="}":
            if lista_final[i+1]== "EXEC" or lista_final[i+1]=="NEW":
                
                i+=1
            elif lista_final[i+1]== "FI" or lista_final[i+1]=="OD":
                i+=1
            elif lista_final[i+1]== "ELSE":
                i+=1
            else:
                r=False
                break
        elif lista_final[i]=="{":
            if lista_final[i+1] in tokens_textuales and lista_final[i+1] not in excepciones :
                i+=1
            elif variable(lista_final[i+1]) and lista_final[i-1]=="EXEC":
                i+=1
            else:
                r=False
                break
    return r





        
            
    
        
            
                
                
                        
                
                
                
            
               
            
        
                
                
        
                
                
        
                
                
                
                    
                    
            
        
        
            
        
            
    
            
            
        
    
    
            
            
        
        
    
    
    

    

    
    


    
    
    
        
            
        
    
    
    
     
                
            
            
            
    
        
    
        

        