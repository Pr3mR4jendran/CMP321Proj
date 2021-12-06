#Prolog Parser

import re

class ParseError(Exception):
    def __init__(self, s):
        print(s) #Prints the specific type of error encountered (text to be passed into the init method of exception class)

def special(c):
   if c in ["+","-","*","/","\\","^","~",":",".","?"," ","#","$","&"]:
       return True
   else :
       raise ParseError("Special character not found")

def digit(c):
    c=re.search("^[0-9]$",c)
    if c:
        return True
    else :
        raise ParseError("Digit not found")
   
def lowercasechar(c):
    c=re.search("^[a-z]$",c)
    if c:
        return True
    else :
        raise ParseError("Lowercase character not found")
    
def uppercasechar(c):
    c=re.search("^[A-Z]$",c)
    if c:
        return True
    else :
        raise ParseError("Uppercase character not found")
    
def numeral(c):
    if digit(c):
        return True
    elif digit(c[0]) and numeral(c[1:]):
        return True
    raise ParseError("Numeral not found")

def alphanumeric(c):
    if lowercasechar(c) or uppercasechar(c) or digit(c):
        return True
    raise ParseError("Alphanumeric character not found")
        
def character(c):
    if alphanumeric(c) or special(c):
        return True
    raise ParseError("Character not found")
    
def string(c):
    if character(c):
        return True
    elif character(c[0]) and string(c[1:]):
        return True
    raise ParseError("String not found")

def characterlist(c):
    if alphanumeric(c):
        return True
    elif alphanumeric(c[0]) and characterlist(c[1:]):
        return True
    raise ParseError("Character list not found")
    
def variable(c):
    if uppercasechar(c):
        return True
    elif uppercasechar(c[0]) and characterlist(c[1:]):
        return True
    raise ParseError("Variable not found")
    
def smallatom(c):
    if lowercasechar(c):
        return True
    elif lowercasechar(c[0]) and characterlist(c[1:]):
        return True
    raise ParseError("Small atom not found")