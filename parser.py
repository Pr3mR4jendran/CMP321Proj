import os
import re
import token

lexeme = []   
next_token = -100
total_lines = 1
c_index = -1     
c_next = ""
f_input = None
c_type = -100
errors_count = 0
errors_list = []


lowercase_char, uppercase_char, digit, special = 0, 1, 2, 3
undefined = 99


#   token codes
dash = 32
comma = token.COMMA
open_parenthesis, close_parenthesis = token.LPAR, token.RPAR
quotation = 37
tilde, colon, period, question_mark = token.TILDE,token.COLON, token.DOT, 109
addition_op, subtraction_op, multiplication_op, division_op = token.PLUS, token.MINUS, token.STAR, token.SLASH
backslash, circumflex = 105, token.CIRCUMFLEX
hashtag, dollar_sign, ampersand,space = 111,112,113,114
EOF = -99

spchar_list =["+","-","*","/","\\","^","~",":",".","?"," ","#","$","&"]

#lookup table
def find(character): 
    
    global c_index, next_token, total_lines   
    if character == '.':
        lexeme.append(c_next)
        next_token = period
        
    elif character == '-':
         lexeme.append(c_next)
         next_token = dash
        
    elif character == '?':
        lexeme.append(c_next)
        next_token = question_mark
        
    elif character == '\'':
        lexeme.append(c_next)
        next_token = quotation
        
        
    elif character == '(':
        lexeme.append(c_next)
        next_token = open_parenthesis
    elif character == ')':
        lexeme.append(c_next)
        next_token = close_parenthesis
        
    elif character == ':':
          lexeme.append(c_next)
          next_token = colon
                   
    elif character == "\n":
          total_lines += 1
          c_index = -1
                  
    elif character == ',':
         lexeme.append(c_next)
         next_token = comma
           
    elif character != '':
         lexeme.append(c_next)
         next_token = undefined
    
    elif character in spchar_list:
        lexeme.append(c_next)
        next_token = spchar_list.index(character)+69
   
    else:
        lexeme.append(c_next)
        next_token = EOF

    return next_token


def get_char():
    global c_next, c_type, c_index, total_lines
    c_next = f_input.read(1)   
    if c_next != '': # c_next becomes empty when file ends
        while re.match("\s", c_next):     
            if c_next == "\n":
                total_lines += 1
                c_index = -1
            else:
                c_index += 1
            c_next = f_input.read(1)

        if re.match("\d", c_next):    
            c_type = digit
        elif re.match("[A-Z_]", c_next):  
            c_type = uppercase_char
        elif re.match("[a-z]", c_next): 
            c_type = lowercase_char
        
        else:
            c_type = undefined
            
    else: # reach this condition  after file has ended 
        c_type = EOF  

    c_index += 1

def lex():
    global lexeme
    global next_token
    lexeme = []
    if c_type==digit:
        lexeme.append(c_next)
        get_char()
        while c_type == digit:
            lexeme.append(c_next)
            get_char()
        next_token = digit
        
    elif c_type == lowercase_char:
        lexeme.append(c_next)
        get_char()
        while  c_type == lowercase_char or c_type == uppercase_char or c_type == digit:
            lexeme.append(c_next)
            get_char()
        next_token = lowercase_char
       
    elif c_type == uppercase_char:
        lexeme.append(c_next)
        get_char()
        while  c_type == lowercase_char or c_type == uppercase_char or c_type == digit:
            lexeme.append(c_next)
            get_char()
        next_token = uppercase_char
        
    elif c_type == undefined:
        find(c_next)
        get_char()
    elif c_type == EOF:
        lexeme.append("EOF")

    return next_token


#<special> -> + | - | * | / | \ | ^ | ~ | : | . | ? | | # | $ | &
def special():
    global errors_count, errors_list
    if next_token in [x+69 for x in range(len(spchar_list))]:# x+69 used to validate special charecter
        lex()
    else:
        errors_list.append(("Special Character used is not valid", total_lines, c_index))
        errors_count += 1
        get_char()
        lex()

#<alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>
def alphahnum():
    global errors_count, errors_list
    if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
        lex()
    else:
        errors_count += 1
        errors_list.append(("Alphanumeric Character used is not valid", total_lines, c_index))
        get_char()
        lex()

#<numeral> -> <digit> | <digit> <numeral>
def numeral():
    global errors_count, errors_list
    if next_token == digit:     
        lex()
        if next_token == digit:  
            numeral()
    else:
        errors_count += 1
        errors_list.append(("Numeral used is not valid ", total_lines, c_index))
        get_char()
        lex()

# <character> -> <alphanumeric> | <special>
def character():
    global errors_count, errors_list
    if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
        alphahnum()
    elif next_token in [x+69 for x in range(len(spchar_list))]:  
        special()
    else:
        errors_count += 1
        errors_list.append(("Character used is invalid", total_lines, c_index))
        get_char()
        lex()
        
        
# <string> -> <character> | <character> <string>
def string():
    character()       
    if  next_token == lowercase_char or next_token == uppercase_char or next_token == digit or next_token in [x+69 for x in range(len(spchar_list))]:
        lex()
        string()


#<character-list> -> <alphanumeric> | <alphanumeric> <character-list> 
def characterlist():
    alphahnum()    
    if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
        lex()
        characterlist()

#<variable> -> <uppercase-char> | <uppercase-char> <character-list> 
def variable():
    global errors_count, errors_list, next_token
    if next_token == uppercase_char:        
        lex()
        if  next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
            characterlist()
        elif next_token == dash:
            errors_count += 1
            errors_list.append(("Variable name used is invalid", total_lines, c_index))
            get_char()
            lex()

    else:
        errors_count += 1
        errors_list.append(("Variable name must begin with uppercase", total_lines, c_index))
        get_char()
        lex()

#<small-atom> -> <lowercase-char> | <lowercase-char> <character-list>
def smallatom():
    global errors_count, errors_list
    if next_token == lowercase_char:        
        lex()
        if next_token == lowercase_char or next_token == uppercase_char or next_token == digit:
            characterlist()
    else:
        errors_count += 1
        errors_list.append(("small-atom must begin with lowercase", total_lines, c_index))
        get_char()
        lex()

#<atom> -> <small-atom> | ' <string> '
def atom():
    global errors_count, errors_list

    if next_token == lowercase_char:   
        smallatom()
    elif next_token == quotation:      
        lex()
        string()                  
        if next_token == quotation:     
            lex()
        else:
            errors_count += 1
            errors_list.append(("'' not found in string ", total_lines, c_index))
            get_char()
            lex()
    else:
        errors_count += 1
        errors_list.append(("Atom used in invalid", total_lines, c_index))
        get_char()
        lex()


#<term> -> <atom> | <variable> | <structure> | <numeral>
def term():
    global errors_count, errors_list
    if next_token == digit:    
        numeral()
    elif next_token == uppercase_char:      
        variable()
    elif next_token == lowercase_char or next_token == quotation:  
        structure()
    else:
        errors_count += 1
        errors_list.append(("Term used is invalid", total_lines, c_index))
        get_char()
        lex()

#<term-list> -> <term> | <term> , <term-list>
def termlist():
    global errors_count, errors_list
    term()
    if next_token == comma:
        lex()
        termlist()

#<structure> -> <atom> ( <term-list> )
def structure():  
    global errors_count, errors_list
    atom()        
    if next_token == open_parenthesis:     
        lex()
        termlist()                   
        if next_token == close_parenthesis: 
            lex()
        else:
            errors_count += 1
            errors_list.append(("Structure is missing a closing parenthesis", total_lines, c_index))
            get_char()
            lex()

#<predicate> -> <atom> | <atom> ( <term-list> )
def predicate():
    global errors_count, errors_list
    atom()
    if next_token == open_parenthesis:
        lex()
        termlist()
        if next_token == close_parenthesis:
            lex()
        else:
            errors_count += 1
            errors_list.append(("Predicate doesnt have a closing parenthesis ", total_lines, c_index))
            get_char()
            lex()

#<predicate-list> -> <predicate> | <predicate> , <predicate-list>
def predicatelist():
    global errors_count, errors_list
    predicate()          
    if next_token == comma:     
        lex()
        predicatelist()

#<query> -> ?- <predicate-list> . 
def query():
    global errors_count, errors_list
    if next_token == question_mark:     
        lex()
        if next_token == dash:          
            lex()
            predicatelist()      
            if next_token == period:    
                lex()
            else:
                errors_count += 1
                errors_list.append(("Query has a missing period", total_lines, c_index))
                get_char()
                lex()
        else:
            errors_count += 1
            errors_list.append(("Query is missing -", total_lines, c_index))
            get_char()
            lex()
    else:
        errors_count += 1
        errors_list.append(("Query is missing ?", total_lines, c_index))
        get_char()
        lex()
        
        
# <clause> -> <predicate> . | <predicate> :- <predicate-list> .       
def clause():
    global errors_count, errors_list
    predicate()               
    if next_token == period:        
        lex()
    elif next_token == colon:      
        lex()
        if next_token == dash:      
            lex()
            predicatelist()  
            if next_token == period:  
                lex()
            else:
                errors_count += 1
                errors_list.append(("Clause ending missing a period", total_lines, c_index))
                get_char()
                lex()
        else:
            errors_count += 1
            errors_list.append(("Clause missing colon", total_lines, c_index))
            get_char()
            lex()

    else:
        errors_count += 1
        errors_list.append(("Clause is invalid", total_lines, c_index))
        get_char()
        lex()

#<clause-list> -> <clause> | <clause> <clause-list> 
def clauselist():
    global errors_count, errors_list
    clause()   
    if next_token == lowercase_char or next_token == quotation:     
        clauselist()



#<program> -> <clause-list> <query> | <query>
def program():
    global errors_count, errors_list
    if next_token == question_mark:   
        query()
    elif next_token == lowercase_char: 
        clauselist()
        if next_token == question_mark:    
            query()
        else:
            errors_count += 1
            errors_list.append(("Program is not valid as clause list is not followed by a query", total_lines, c_index))
            get_char()
            lex()


def display_errors(f_output):
    global errors_list
    print("Number of Errors in this file =",errors_count)
    f_output.write("Number of Errors in this file = "+str(errors_count)+"\n")
    for e in errors_list:
        print("Error :", e[0],".This error is found in line",e[1],"at index " ,e[2]-1)
        f_output.write("Error : "+str(e[0])+".This error is found in line "+str(e[1])+" at index "+str(e[2]-1)+"\n")
        
        
        
    
        
def mainfunction():
    #Making a list of all the input files(numbered files) from all the files in the current directory
    flist = sorted([file for file in os.listdir(os.getcwd()) if file[-4::] == ".txt" and file.split(".")[0].isdigit()])     
    #Filters list to make sure the file numbers remaining are sequential
    counter=1
    for file in flist:
        if int(file.split(".")[0])!=counter:
            flist=flist[:counter-1]
            break
        counter+=1
  
    if len(flist) == 0:
        print("Valid input files not found in the Directory")
   
    f_output = open("parser_output.txt", "w")

    global f_input, c_next,c_index, c_type, errors_count, errors_list, next_token, total_lines

    if len(flist) == 0:
        print("Valid input files not found in the Directory")

    for file in flist:
        try:
            f_input = open(file, "r")
            print("\nParsing the File  :",file)
            f_output.write("\nParsing the File: " + file + "\n")

            get_char()

            while c_type != EOF:
                lex()
                program()

            if not errors_list:
                print("There are no Errors. Nice Program :)")
                f_output.write("There are no Errors. Nice Program :)\n")
               
            else:
                display_errors(f_output)

            
            errors_count = 0 #setting intial number of errors for next file
            total_lines = 1
            errors_list = []
            next_token = -100 if file != flist[-1] else EOF
            c_index = -1

        except FileNotFoundError:
            print("Cannot open the file !: " + file)
            f_output.write("Cannot open the file: " + file + "\n")
    f_input.close()


#Calling the main function to run the parse on all the files
mainfunction()
