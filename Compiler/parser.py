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
        else: 
            #we had an error
            index += 1 #we should halt execution and dig up the error but until then let's just skip ahead
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
    types = ["int", "double", "bool","string", "void"]
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

    functionDecl.formalsList = checkFormals() 

    #check RParen
    if not checkRParen():
        index = originalIndex
        return functionDecl

    functionDecl.stmtBlock = checkStmtBlock() #this is where we need to work from next



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
        variableClass = checkVariable()
        if variableClass.finished and variableClass.typeClass.name != "void":
            variablesList.append(variableClass)
        else:
            doneWithFormals = True
        
        if checkComma():
            doneWithFormals = False
        else:
            doneWithFormals = True

    return variablesList

def checkStmtBlock():
    global tokenList
    global index
    originalIndex = index
    stmtBlockClass = StmtBlockClass()
    if not checkLCurly():
        return stmtBlockClass

    #get any number of variables declarations
    doneWithVariableDecls = False
    while not doneWithVariableDecls:
        variableDecl = checkVariableDecl()
        if variableDecl.finished:
            stmtBlockClass.variableDecls.append(variableDecl)
        else:
            doneWithVariableDecls = True

    doneWithStmts = False

    while not doneWithStmts:
        stmt = checkStmt()

        if stmt.finished:
            stmtBlockClass.stmts.append(stmt)
        else:
            doneWithStmts = True


    #get any number of statements

    if not checkRCurly():
        return stmtBlockClass

    #we closed our curly, return complete stmt block
    stmtBlockClass.finished = True
    return stmtBlockClass



#WE STOPPPED HERE
def checkStmt():
    global tokenList
    global index
    stmt = StmtClass()
    stmt.expr = checkExpr()
    if stmt.expr.finished:
        if checkSemiColon():
            stmt.finished = True

    return stmt
    

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
    #check pre characters
    global tokenList
    global index
    originalIndex = index
    exprTree = ExprTree()
    expr = exprBuilder(exprTree)


    return expr



    #we generate a tree, and then we return the root

    # expr = ExprClass()
    # ident = checkIdent()

    # if prevExpr == None:
    #     if ident.finished: #we found a valid  ident
    #         if checkOp():
    #             expr.operator = tokenList[index].text
    #             expr.leftIdent = ident
    #             index+=1
    #             return checkExpr(prevExpr)
    #     else:
    #         return ident #we failed
    # else:
    #     if ident.finished:
    #         prevExpr.rightIdent = ident
    #         #check for another op, return completed otherwise
    #         if not checkOp():
    #             prevExpr.finished = True
    #             index += 1
    #             return prevExpr
    #         else: 
    #             #we need to make a new expr out of the new operator, if op code is GREATER
    #             expr.operator = tokenList[index].text
    #             expr.leftIdent = ident

    #             prevExpr.rightIdent = None
    #             prevExpr.rightExpr = checkExpr(expr)

    #             if prevExpr.rightExpr.finished == True:
    #                 prevExpr.finished = True
    #                 return prevExpr


#we need to increment our index here!
def exprBuilder(exprTree):
    global tokenList
    global index
    expr = ExprClass()
    buildingTree = True
    #print("START INDEX " + str(index))

    while buildingTree:
        if exprTree.root == None:
            exprTree.root = ExprClass()
            exprTree.nicoRobin = exprTree.root
        #now let's start
        ident = checkIdent()
        if ident.finished == True:
            if not checkOp(): #we don't find another operator
                #if we have a parent, set their right child to the ident
                if exprTree.nicoRobin.parent != None:
                    exprTree.nicoRobin.parent.rightChild = ident
                else: #otherwise, make the root the ident, we might need an error here
                    exprTree.root = ident

                exprTree.root.finished = True
                buildingTree = False #we done
            else: #we found another operator
                if exprTree.nicoRobin.parent == None or opLevel(tokenList[index].text) > opLevel(exprTree.nicoRobin.parent.operator): #we're higher priority already, or no parent
                    exprTree.nicoRobin.operator = tokenList[index].text
                    exprTree.nicoRobin.leftChild = ident
                    exprTree.nicoRobin.rightChild = ExprClass()
                    exprTree.nicoRobin.rightChild.parent = exprTree.nicoRobin
                    exprTree.nicoRobin = exprTree.nicoRobin.rightChild
                    index += 1
                else:
                    exprTree.nicoRobin.parent.rightChild = ident 
                    exprTree.nicoRobin.operator = tokenList[index].text
                    #move up until we find one which is better than us
                    interestExpr = exprTree.nicoRobin.parent
                    while(interestExpr.parent != None and opLevel(exprTree.nicoRobin.operator) <= opLevel(interestExpr.parent.operator) ):
                        interestExpr = interestExpr.parent

                    #get new nodes parent, tell parent new child is new node
                    exprTree.nicoRobin.parent = interestExpr.parent

                    if exprTree.nicoRobin.parent != None:
                        exprTree.nicoRobin.parent.rightChild = exprTree.nicoRobin

                    #make replaced node child, tell child we're the new parent
                    exprTree.nicoRobin.leftChild = interestExpr
                    exprTree.nicoRobin.leftChild.parent = exprTree.nicoRobin

                    if exprTree.nicoRobin.parent == None:
                        #yoinks scoob, like, we're the new root
                        exprTree.root = exprTree.nicoRobin

                    exprTree.nicoRobin.rightChild = ExprClass()
                    exprTree.nicoRobin.rightChild.parent = exprTree.nicoRobin
                    exprTree.nicoRobin = exprTree.nicoRobin.rightChild

                    index += 1
        else:
            buildingTree = False

    #print("END INDEX " + str(index))
    return exprTree.root



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
    constant = ConstantClass()

    if "Constant" in tokenList[index].flavor:
        constant.name = tokenList[index].text
        constant.constantType = tokenList[index].flavor
        constant.finished = True 
        index += 1
        return constant
    elif "null" in tokenList[index].flavor:
        constant.finished = True
        constant.name = "null"
        constant.constantType = "null"
        index += 1
        return constant
    else:   
        return constant

#Helpers-----------------------------

def checkLParen():
    global index
    global tokenList
    if tokenList[index].text == "(":
        index+=1
        return True
    return False

def checkRParen():
    global index
    global tokenList
    if tokenList[index].text == ")":
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
    print(tokenList[index].text + " this is it")
    if tokenList[index].text == ";":
        print("WOWOWOWOWOW")
        index+=1
        return True
    return False

def checkVoid():
    global tokenList
    global index
    if tokenList[index].text == "void":
        index += 1
        return True
    return False

def checkComma():
    global tokenList
    global index
    if tokenList[index].text == ",":
        index += 1
        return True
    return False

def checkLCurly():
    global tokenList
    global index
    if tokenList[index].text == "{":
        index += 1
        return True
    return False

def checkRCurly():
    global tokenList
    global index
    if tokenList[index].text == "}":
        index += 1
        return True
    return False

def checkExMark():
    global tokenList
    global index
    if tokenList[index].text == "!":
        index += 1
        return True
    return False

def checkThis():
    global tokenList
    global index
    if tokenList[index].text == "this":
        index += 1
        return True
    return False

def checkMiddleExprOp():
    global tokenList
    global index
    middleOps = ["+","-","*","/","%","<","<=",">",">=","==","!=", "&&","||"]
    if tokenList[index].text in middleOps:
        index += 1
        return True
    return False

def checkMinus():
    global tokenList
    global index
    if tokenList[index].text == "-":
        index += 1
        return True
    return False    

def checkOp():
    global tokenList
    global index
    allOps = ["=","||","&&","==","!=","<","<=",">",">=","+","-","*","/","%","!"]
    if tokenList[index].text in allOps:
        return True
    else:
        return False


def opLevel(op):
    level0 = ["="]
    level1 = ["||"]
    level2 = ["&&"]
    level3 = ["==","!="]
    level4 = ["<","<=",">",">="]
    level5 = ["+","-"]
    level6 = ["*","/","%"]
    level7 = ["!"]
    if op in level0:
        return 0
    elif op in level1:
        return 1
    elif op in level2:
        return 2
    elif op in level3:
        return 3
    elif op in level4:
        return 4
    elif op in level5:
        return 5
    elif op in level6:
        return 6
    elif op in level7:
        return 7
    else:
        return -1

