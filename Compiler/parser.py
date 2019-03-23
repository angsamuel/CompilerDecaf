from token import Token
import parserClasses
from parserClasses import *
import random

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

    #check LParen
    if not checkLParen():
        index = originalIndex
        return functionDecl

    functionDecl.formalsList = checkFormals() 

    #check RParen
    if not checkRParen():
        index = originalIndex
        return functionDecl

    stmtBlock = checkStmtBlock() #this is where we need to work from next

    if stmtBlock.finished:
        functionDecl.stmtBlock = stmtBlock
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
    randNum = random.randint(1,1000)
    global tokenList
    global index
    #print tokenList[index].text

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
            #print("HEYA")
            stmtBlockClass.stmts.append(stmt)
            #print(len(stmtBlockClass.stmts))
            #print(len(stmtBlockClass.stmts))
            #print("-----")
        else:
            doneWithStmts = True

    #get any number of statements

    if not checkRCurly():
        index = originalIndex
        return stmtBlockClass


    #we closed our curly, return complete stmt block
    stmtBlockClass.finished = True
    return stmtBlockClass



#WE STOPPPED HERE
def checkStmt():
    global tokenList
    global index
    stmt = StmtClass()
    originalIndex = index
    
    expr = checkExpr()
    if expr.finished:
        if checkSemiColon():
            stmt.expr = expr
            stmt.finished = True
            return stmt
    else:
        index = originalIndex

    #check ifstatement

    ifStmt = checkIfStmt()
    if ifStmt.finished:
        return ifStmt
    else:
        index = originalIndex

    stmtBlock = checkStmtBlock()
    if stmtBlock.finished:
        return stmtBlock
    else:
        index = originalIndex

    # #check while statement
    # whileStmt = checkWhileStmt()
    # if whileStmt.finished:
    #     return whileStmt

    # #check for statement
    # forStmt = checkForStmt()
    # if forStmt.finished:
    #     return forStmt

    # #check breakstmt
    # breakStmt = checkBreakStmt()
    # if breakStmt.finished:
    #     return breakStmt

    # #check return statement
    # returnStmt = checkReturnStmt()
    # if returnStmt.finished:
    #     return returnStmt

    # #check print statement
    # printStmt = checkPrintStmt()
    # if printStmt.finished:
    #     return printStmt

    # #check stmt block
    # stmtBlock = checkStmtBlock()
    # if stmtBlock.finished:
    #     return stmtBlock



    return stmt
    

def checkIfStmt():
    global tokenList
    global index
    originalIndex = index
    ifStmt = IfStmtClass()
    if tokenList[index].text == "if":
        index += 1
        if checkLParen():
            expr = checkExpr()
            if expr.finished:
                ifStmt.expr = expr
                if checkRParen():
                    thenStmt = checkStmt()
                    if thenStmt.finished:
                        ifStmt.thenStmt = thenStmt
                        ifStmt.finished = True
    if ifStmt.finished:
        originalIndex = index
    else:
        index = originalIndex

    if ifStmt.finished: #now we gotta check for the else
        if tokenList[index].text == "else":
            index+=1
            print("WELL NOW")
            elseStmt = checkStmt()
            print("WELL NOW")
            if elseStmt.finished:
                ifStmt.elseStmt = elseStmt
            else: 
                index = originalIndex
    return ifStmt

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



#we need to increment our index here!
def exprBuilder(exprTree):
    global tokenList
    global index
    originalIndex = index
    expr = ExprClass()
    buildingTree = True
    firstLoop = True
    #print("START INDEX " + str(index))


    while buildingTree:
        hardValue = None

        if exprTree.root == None:
            exprTree.root = ExprClass()
            exprTree.nicoRobin = exprTree.root
        #now let's start
        hardValue = checkIdent()

        if not firstLoop and hardValue.finished == False:
            hardValue = checkConstant()



        if hardValue.finished == True:
            if not checkOp(): #we don't find another operator
                #if we have a parent, set their right child to the ident
                if exprTree.nicoRobin.parent != None:
                    exprTree.nicoRobin.parent.rightChild = hardValue
                else: #otherwise, make the root the ident, we might need an error here
                    exprTree.root = hardValue

                exprTree.root.finished = True
                buildingTree = False #we done
            else: #we found another operator
                if exprTree.nicoRobin.parent == None or opLevel(tokenList[index].text) > opLevel(exprTree.nicoRobin.parent.operator): #we're higher priority already, or no parent
                    exprTree.nicoRobin.operator = tokenList[index].text
                    exprTree.nicoRobin.leftChild = hardValue
                    exprTree.nicoRobin.rightChild = ExprClass()
                    exprTree.nicoRobin.rightChild.parent = exprTree.nicoRobin
                    exprTree.nicoRobin = exprTree.nicoRobin.rightChild
                    index += 1
                else:
                    exprTree.nicoRobin.parent.rightChild = hardValue 
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
            #exprTree.root.finished = False
            #index = originalIndex
            #return exprTree.root
        firstLoop = False

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
        constant.constantType = tokenList[index].flavor.replace("T_","")
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
    if tokenList[index].text == ";":
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

