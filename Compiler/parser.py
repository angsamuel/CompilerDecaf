from token import Token
import parserClasses

tokenList = []
index = 0
ir = [] #intermediate representation


def parseTokenList(_tokenList):
    global tokenList
    global index
    tokenList = _tokenList
    index = 0

    while index < len(tokenList):
        checkDecl()

def checkDecl():
    global tokenList
    global index
    index += 1
    return True

def checkVariableDecl():
    global tokenList
    global index
    originalIndex = index
    if checkVariable() and checkSemiColon():
        return True
    else:
        index = originalIndex
        return False

def checkVariable():
    global tokenList
    global index
    originalIndex = index
    if checkType() and checkIdent():
        return True
    else:
        index = originalIndex
        return False


def checkType():
    global tokenList
    global index
    types = ["int", "double", "bool","string"]
    if tokenList[index].name in types:
        index += 1
        return True
    else:
        return False

def checkFunctionDecl():
    global tokenList
    global index
    originalIndex = index
    if (checkVoid() or checkType()) and checkIdent() and checkLParen() and checkRParen() and checkStmtBlock():
        return True
    else:
        index = originalIndex
        return False


def checkFormals():
    global tokenList
    global index
    originalIndex = index
    doneWithFormals = False
    while not doneWithFormals:
        #if don't have a variable then we've struck an error
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
                else 
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
    global index
    global tokenList
    if "Identifier" in tokenList[index].flavor:
        index += 1
        return True
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
    return checkLValue()

def checkSemiColon():
    global tokenList
    global index
    if tokenList[index].name == ";":
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
    middleOps = ["+","-","*","/"."%","<","<=",">",">=","==","!=", "&&","||"]
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
