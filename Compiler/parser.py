from token import Token
import parserClasses
from parserClasses import *

tokenList = []
index = 0
ir = [] #intermediate representation
tabCount = 0

def printAST():
    global tabCount
    print("Program:")
    tabCount = 1
    for thing in ir:
        thing.printMyStuff(tabCount)



def parseTokenList(_tokenList):
    global tokenList
    global index
    tokenList = _tokenList
    index = 0
    while index < len(tokenList):
        irObject = checkDecl()
        if irObject.finished:
            ir.append(irObject)
    printAST()

def checkDecl():
    global tokenList
    global index
    functionDecl = checkFunctionDecl()
    if functionDecl.finished:
        return functionDecl
    else:
        variableDecl = checkVariableDecl()
        return variableDecl

def checkVariableDecl():
    global tokenList
    global index
    originalIndex = index

    #create new variable decl
    variableDecl = VariableDeclClass()

    #check for a variable
    variable = checkVariable()

    #if we got a var, and a semicolon, add the var and finish
    if variable.finished and checkSemiColon():
        variableDecl.variableClass = variable
        variableDecl.finished = True
    else: #else we gotta backtrack
        index = originalIndex
    
    return variableDecl


def checkVariable():
    global tokenList
    global index
    originalIndex = index
    variable = VariableClass()
    
    typeClass = checkType()

    if typeClass.finished:
        ident = checkIdent()
        if ident.finished:
            variable.typeClass = typeClass
            variable.identClass = ident
            variable.finished = True
    else:
        index = originalIndex    
    return variable


def checkType():
    global tokenList
    global index
    types = ["int", "double", "bool","string","void"]
    typeClass = TypeClass()
    if tokenList[index].text in types:
        typeClass.name = tokenList[index].text
        typeClass.finished = True
        index += 1
    return typeClass

def checkFunctionDecl():
    global tokenList
    global index
    originalIndex = index
    functionDecl = FunctionDeclClass()
    
    #get our type
    typeClass = checkType()
    if typeClass.finished:
        functionDecl.typeClass = typeClass
    else:
        index = originalIndex
        return functionDecl

    #get our ident
    identClass = checkIdent()
    if identClass.finished:
        functionDecl.ident = identClass
    else:
        index = originalIndex
        return functionDecl

    #check LParent
    if not checkLParen():
        index = originalIndex
        return functionDecl

    functionDecl.formals = checkFormals() 

    #check RParen
    if not checkRParen():
        index = originalIndex
        return functionDecl

    if not checkLCurly():
        index = originalIndex
        return functionDecl

    #functionDecl.stmtBlock = checkStmtBlock() #this is where we need to work from next

    if not checkRCurly():
        index = originalIndex
        return functionDecl

    functionDecl.finished = True #we have everything we need
    return functionDecl

def checkFormals(): #returns a variabls list
    global tokenList
    global index
    originalIndex = index
    variablesList = [] #list of parameters we'll return 
    doneWithFormals = False
    while not doneWithFormals:
        #if don't have a variable then we've struck an error
        variableClass
        if not checkVariable():
            doneWithFormals = True
            index = originalIndex
            return False
        else:
            if not checkComma():
                doneWithFormals = True
    return True

def checkStmtBlock():
    global tokenList
    global index
    originalIndex = index
    if checkLCurly(): #we must have a curly brace
        while checkVariableDecl():
            keep = "checking"

        doneCheckingStmts = False
        while not doneCheckingStmts:
            if not checkStmt():
                doneCheckingStmts = True
                if checkRCurly():
                    return True
                else: 
                    index = originalIndex
                    return False
    else:
        index = originalIndex
        return False


#WE STOPPPED HERE
def checkStmt():
    global tokenList
    global index
    return True

def checkIfStmt():
    global tokenList
    global index
    return True

def checkWhileStmt():
    global tokenList
    global index
    return True

def checkForStmt():
    global tokenList
    global index
    return True

def checkReturnStmt():
    global tokenList
    global index
    return True

#check break value
def checkBreakStmt():
    global tokenList
    global index
    if tokenList[index].name == "break" and tokenList[index+1] == ";":
        index+=2
        return True
    return False

def checkPrintStmt():
    global tokenList
    global index
    return True

def checkExpr():
    starters = ["(", "!"]
    global tokenList
    global index
    originalIndex = index
    completedSingleExpr = False
    if checkLParen():
        if checkExpr(): #call down
            if checkRParen():
                completedSingleExpr = True
            else:
                index = originalIndex
                return False
        return False
    elif checkExMark():
        return checkExpr()
    elif checkMinus():
        return checkExpr()
    elif checkThis():
        completedSingleExpr = True
    elif checkConstant():
        completedSingleExpr = True
    elif checkLValue():
        completedSingleExpr = True

    #if we completed something
    if completedSingleExpr:
        g = 1
        #check next position for one of the symbols
        if checkMiddleExprOp():
            return checkExpr()
        else:
            return True
    else:
        index = originalIndex
        return False

def checkLValue():
    return False

def checkCall():
    global index
    global tokenList
    return checkIdent() and checkLParen() and checkActuals() and checkRParen()

#***
def checkActuals():
    global index
    global tokenList
    return True

def checkConstant():
    global index
    global tokenList
    if "Constant" in tokenList[index].flavor:
        index += 1
        return True
    elif "null" in tokenList[index].flavor:
        index += 1
        return True
    else:   
        return False


#Helpers-----------------------------

def checkLParen():
    global index
    global tokenList
    if tokenList[L].name == "(":
        index+=1
        return True
    return False

def checkRParen():
    global index
    global tokenList
    if tokenList[index].name == ")":
        index += 1
        return True
    return False

def checkIdent():
    global index
    global tokenList
    ident = IdentClass()
    if "Identifier" in tokenList[index].flavor:
        ident.name = tokenList[index].text
        ident.finished = True
        index += 1
    return ident

def checkSemiColon():
    global tokenList
    global index
    if tokenList[index].text == ";":
        index+=1
        return True
    return False

def checkVoid():
    global tokenList
    global index
    if tokenList[index].name == "void":
        index += 1
        return True
    return False

def checkComma():
    global tokenList
    global index
    if tokenList[index].name == ",":
        index += 1
        return True
    return False

def checkLCurly():
    global tokenList
    global index
    if tokenList[index].name == "{":
        index += 1
        return True
    return False

def checkRCurly():
    global tokenList
    global index
    if tokenList[index].name == "}":
        index += 1
        return True
    return False

def checkExMark():
    global tokenList
    global index
    if tokenList[index].name == "!":
        index += 1
        return True
    return False

def checkThis():
    global tokenList
    global index
    if tokenList[index].name == "this":
        index += 1
        return True
    return False

def checkMiddleExprOp():
    global tokenList
    global index
    middleOps = ["+","-","*","/","%","<","<=",">",">=","==","!=", "&&","||"]
    if tokenList[index].name in middleOps:
        index += 1
        return True
    return False

def checkMinus():
    global tokenList
    global index
    if tokenList[index].name == "-":
        index += 1
        return True
    return False    
