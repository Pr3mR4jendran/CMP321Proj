#Prolog Parser

import re


def special(c):
   if c in ["+","-","*","/","\\","^","~",":",".","?"," ","#","$","&"]:
       return True
   else :
       return False

def digit(c):
    c=re.search("^[0-9]$",c)
    if c:
        return True
    else :
        return False
   
def lowercasechar(c):
    c=re.search("^[a-z]$",c)
    if c:
        return True
    else :
        return False
    
def uppercasechar(c):
    c=re.search("^[A-Z]$",c)
    if c:
        return True
    else :
        return False
    
def numeral(c):
    if digit(c):
        return True
    elif digit(c[0]) and numeral(c[1:]):
        return True
    return False

def alphanumeric(c):
    if lowercasechar(c) or uppercasechar(c) or digit(c):
        return True
    return False
        
def character(c):
    if alphanumeric(c) or special(c):
        return True
    return False
    
def string(c):
    if character(c):
        return True
    elif character(c[0]) and string(c[1:]):
        return True
    return False

def characterlist(c):
    if alphanumeric(c):
        return True
    elif alphanumeric(c[0]) and characterlist(c[1:]):
        return True
    return False
    
def variable(c):
    if uppercasechar(c):
        return True
    elif uppercasechar(c[0]) and characterlist(c[1:]):
        return True
    return False
    
def smallatom(c):
    if lowercasechar(c):
        return True
    elif lowercasechar(c[0]) and characterlist(c[1:]):
        return True
    return False
    
