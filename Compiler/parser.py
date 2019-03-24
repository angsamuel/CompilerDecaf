from token import Token
import parserClasses
from parserClasses import *
import sys

tokenList = []
index = 0
ir = [] #intermediate representation
tabCount = 0
parenBonus = 0
whileScore = 0
forScore = 0

def printAST():
    global tabCount
    print ""
    print("Program:")
    tabCount = 1
    for thing in ir:
        thing.printMyStuff("",tabCount)

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
    print("HEE HAW")
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
            #print error here
            printError(index)
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
            stmtBlockClass.stmts.append(stmt)
        else:
            doneWithStmts = True

    #get any number of statements

    if not checkRCurly():
        printError(index)
        index = originalIndex
        return stmtBlockClass


    #we closed our curly, return complete stmt block
    stmtBlockClass.finished = True
    return stmtBlockClass


def parenBonusCheck():
    global tokenList
    global index
    global parenBonus
    #print tokenList[index].text
    if checkLParen():
        parenBonus += 10
        #print tokenList[index].text
        parenBonusCheck()
    elif parenBonus > 0  and checkRParen():
        parenBonus -= 10
        parenBonusCheck()
        #else:
            #we'll handle parenthesis mismatch check elsewhere
            

#WE STOPPPED HERE
def checkStmt():
    global tokenList
    global index
    stmt = StmtClass()
    originalIndex = index

    if checkOptionalSemiColon():
        stmt.finished = True
        stmt.expr = None
        return stmt
    
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

    whileStmt = checkWhileStmt()
    if whileStmt.finished:
        return whileStmt


    #check for statement
    forStmt = checkForStmt()
    if forStmt.finished:
        return forStmt

    # #check breakstmt
    breakStmt = checkBreakStmt()
    if breakStmt.finished:
        return breakStmt
    else:
        index = originalIndex

    #check return statement
    returnStmt = checkReturnStmt()
    if returnStmt.finished:
        return returnStmt
    else:
        index = originalIndex

    #check print statement
    printStmt = checkPrintStmt()
    if printStmt.finished:
        return printStmt
    else:
        index = originalIndex

    stmtBlock = checkStmtBlock()
    if stmtBlock.finished:
        return stmtBlock
    else:
        index = originalIndex




    return stmt



def checkPrintStmt():
    global tokenList
    global index
    printStmt = PrintStmtClass()
    originalIndex = index
    if tokenList[index].text == "Print":
        index += 1
        if checkLParen():
            #we need to grab our expressions
            doneWithExprs = False
            while not doneWithExprs:
                expr = checkExpr()
                if expr.finished:
                    printStmt.exprs.append(expr)
                else:
                    doneWithExprs = True
                
                if not checkComma():
                    doneWithExprs = True
            print("YIKES")
            if checkRParen() and checkSemiColon() and len(printStmt.exprs) > 0:
                printStmt.finished = True

    if printStmt.finished == False:
        index = originalIndex
    return printStmt







 
def checkWhileStmt():
    global tokenList
    global index
    global whileScore
    originalIndex = index
    whileStmt = WhileStmtClass()
    if tokenList[index].text == "while": #point of no return
        index += 1
        whileScore += 1
        if checkLParen():
            expr = checkExpr()
            if expr.finished:
                whileStmt.expr = expr
                if checkRParen():
                    bodyStmt = checkStmt()
                    if bodyStmt.finished:
                        whileStmt.bodyStmt = bodyStmt
                        whileStmt.finished = True
                        whileScore -= 1
                else:
                    printError(index)
            else:
                printError(index)
        else:
            printError(index)


    return whileStmt





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
            else:
                printError(index)
    if ifStmt.finished:
        originalIndex = index
    else:
        index = originalIndex

    if ifStmt.finished: #now we gotta check for the else
        if tokenList[index].text == "else":
            index+=1
            elseStmt = checkStmt()
            if elseStmt.finished:
                ifStmt.elseStmt = elseStmt
            else: 
                index = originalIndex
    return ifStmt

def checkReturnStmt():
    global tokenList
    global index
    originalIndex = index
    returnStmt = ReturnStmtClass()
    if tokenList[index].text == "return":
        index += 1
        expr = checkExpr()
        if expr.finished:
            returnStmt.expr = expr
    #print("DEAUX")
        if checkSemiColon():
            returnStmt.finished = True
        else:
            index = originalIndex

    return returnStmt



def checkForStmt():
    global tokenList
    global index
    global forScore
    originalIndex = index
    forStmt = ForStmtClass()
    if tokenList[index].text == "for":
        index += 1
        forScore += 1
        if not checkLParen():
            index = originalIndex
            return forStmt


        leftExpr = checkExpr()
        if leftExpr.finished:
            forStmt.leftExpr = leftExpr

        if not checkSemiColon():
            index = originalIndex
            return forStmt

        middleExpr = checkExpr()

        if middleExpr.finished:
            forStmt.midExpr = middleExpr
        else:
            printError(index)
            index = originalIndex
            return forStmt

        if not checkSemiColon():
            index = originalIndex
            return forStmt

        rightExpr = checkExpr()

        if rightExpr.finished:
            forStmt.rightExpr = rightExpr

        if not checkRParen():
            printError(index)
            index = originalIndex
            return forStmt

        stmt = checkStmt()

        if stmt.finished:
            forStmt.stmt = stmt
            forScore -= 1
            forStmt.finished = True

    return forStmt


#check break value
def checkBreakStmt():
    global tokenList
    global index
    breakStmt = BreakStmtClass()
    if tokenList[index].text == "break":
        if forScore < 1 and whileScore < 1:
            printError(index)
        index+=1
        if checkSemiColon():
            breakStmt.finished = True
    return breakStmt


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
    global parenBonus
    originalIndex = index
    expr = ExprClass()
    buildingTree = True
    firstLoop = True
    #print("START INDEX " + str(index))

    while buildingTree:
        hardValue = None
        parenBonusCheck()

        if exprTree.root == None:
            exprTree.root = ExprClass()
            exprTree.nicoRobin = exprTree.root
        #now let's start

        hardValue = checkCall()

        if not hardValue.finished:
            hardValue = checkIdent()

        #maybe we have a constant?
        if hardValue.finished == False:
            hardValue = checkConstant()

        if hardValue.finished == False:
            hardValue = checkReadThing()

        if hardValue.finished == False:
            parenBonusCheck()
        #this is all unary op stuff
        if hardValue.finished == False and checkUnaryOp():
            #maybe we have a unary operator

            unaryOp = tokenList[index].text
            if exprTree.nicoRobin.parent == None or 7+parenBonus > exprLevel(exprTree.nicoRobin.parent): #add parenthesis to value here
                exprTree.nicoRobin.operator = tokenList[index].text
                exprTree.nicoRobin.score = 7 + parenBonus
                #no left value
                exprTree.nicoRobin.rightChild = ExprClass()
                exprTree.nicoRobin.rightChild.parent = exprTree.nicoRobin
                exprTree.nicoRobin = exprTree.nicoRobin.rightChild
                index+=1
            else: #we need to move this unary up past other unaries
                newNicoRobinParent = exprTree.nicoRobin.parent

                exprTree.nicoRobin.operator = tokenList[index].text
                exprTree.nicoRobin.score = 7 + parenBonus

                interestExpr = exprTree.nicoRobin.parent
                while(interestExpr.parent != None and 7+parenBonus <= exprLevel(interestExpr.parent)):
                    interestExpr = interestExpr.parent

                #slot nico robin in
                exprTree.nicoRobin.parent = interestExpr.parent
                interestExpr.parent.right = exprTree.nicoRobin

                #put the one nico robin replaced under nicorobin

                exprTree.nicoRobin.rightChild = interestExpr
                interestExpr.parent = exprTree.nicoRobin

                #dig to the bottom of the tree and add a new nico robin


                newNicoRobinParent.rightChild = ExprClass()
                exprTree.nicoRobin = newNicoRobinParent.rightChild


        elif hardValue.finished == True:
            parenBonusCheck()
            if not checkOp(): #we don't find another operator
                #if we have a parent, set their right child to the ident
                if exprTree.nicoRobin.parent != None:
                    exprTree.nicoRobin.parent.rightChild = hardValue
                else: #otherwise, make the root the ident, we might need an error here
                    exprTree.root = hardValue

                exprTree.root.finished = True
                buildingTree = False #we done
                return exprTree.root
            else: #we found another operator
                if exprTree.nicoRobin.parent == None or (opLevel(tokenList[index].text) + parenBonus) > exprLevel(exprTree.nicoRobin.parent): #we're higher priority already, or no parent
                    exprTree.nicoRobin.operator = tokenList[index].text
                    
                    exprTree.nicoRobin.score = opLevel(tokenList[index].text) + parenBonus
                    # print("HEE HAW")
                    # print exprTree.nicoRobin.operator
                    # print parenBonus + opLevel(tokenList[index].text)
                    # print("must have been greater than")
                    # print 

                    exprTree.nicoRobin.leftChild = hardValue

                    #check for constant assignment
                    if exprTree.nicoRobin.operator == "=":
                        if exprTree.nicoRobin.leftChild.isConstant:
                            printError(index)


                    exprTree.nicoRobin.rightChild = ExprClass()
                    exprTree.nicoRobin.rightChild.parent = exprTree.nicoRobin
                    exprTree.nicoRobin = exprTree.nicoRobin.rightChild
                    index += 1
                else:
                    exprTree.nicoRobin.parent.rightChild = hardValue 
                    exprTree.nicoRobin.operator = tokenList[index].text
                    if exprTree.nicoRobin.operator == "=":
                        printError(index)
                    exprTree.nicoRobin.score = opLevel(tokenList[index].text) + parenBonus
                    #move up until we find one which is better than us
                    interestExpr = exprTree.nicoRobin.parent
                    

                    while(interestExpr.parent != None and exprLevel(exprTree.nicoRobin) <= exprLevel(interestExpr.parent)):
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
    originalIndex = index
    call = CallClass()



    #print "TOKEN " + tokenList[index].text

    ident = checkIdent()


    if ident.finished:
        #print("YIKES")
        call.ident = ident
        if checkLParen():
            #print("OH NO")
            #get actuals
            gettingActuals = True
            while gettingActuals:
                if checkRParen():
                    gettingActuals = False
                else:
                    expr = checkExpr()
                    if expr.finished:
                        call.actuals.append(expr)
                    if not checkComma():
                        if checkRParen():
                            gettingActuals = False
                        else:
                            index = originalIndex
                            return call #error
        else:
            index = originalIndex
            return call
    else:
        index = originalIndex
        return call

    #print("WHOOPS")
    call.finished = True
    #call.printMyStuff(0)
    return call





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
        if parenBonus > 0:
            printError(index-1)
        return True
    else:
        printError(index)
    return False

def checkOptionalSemiColon():
    global tokenList
    global index
    if tokenList[index].text == ";":
        index+=1
        if parenBonus > 0:
            printError(index-1)
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

def checkUnaryOp():
    global tokenList
    global index
    if tokenList[index].text in ["!","-"]:
        return True
    return False

def exprLevel(expr):
    return expr.score

def opLevel(op):
    global parenBonus
    level0 = ["="]
    level1 = ["||"]
    level2 = ["&&"]
    level3 = ["==","!="]
    level4 = ["<","<=",">",">="]
    level5 = ["+","-"]
    level6 = ["*","/","%"]
    level7 = ["!"]
    if op in level0:
        return 0 + parenBonus
    elif op in level1:
        return 1 + parenBonus
    elif op in level2:
        return 2 + parenBonus
    elif op in level3:
        return 3 + parenBonus
    elif op in level4:
        return 4 + parenBonus
    elif op in level5:
        return 5 + parenBonus
    elif op in level6:
        return 6 + parenBonus
    elif op in level7:
        return 7 + parenBonus
    else:
        return -1

def checkReadThing():
    global tokenList
    global index
    originalIndex = index
    if tokenList[index].text == "ReadInteger":
        index+=1
        if checkLParen() and checkRParen():
            checkReadClass = ReadIntegerClass()
            checkReadClass.finished = True
            return checkReadClass
    elif tokenList[index].text == "ReadLine":
        index+=1
        if checkLParen() and checkRParen():
            checkLineClass = ReadLineClass()
            checkLineClass.finished = True
            return checkLineClass

    index = originalIndex
    return ReadLineClass()



def printError(i):
    global tokenList
    preSpaceCount = 0
    currentTokenIndex = 0
    countingSpaces = True
    print ""
    print "*** Error line " + str(tokenList[i].line) + "."
    lineString = ""

    for token in tokenList:
        if currentTokenIndex == i:
            countingSpaces = False

        if token.line == tokenList[i].line:
            lineString += token.text + " "
            if countingSpaces:
                    #print("ADDING " + str((len(tokenList[i].text) + 1)))
                    #print str(len(tokenList[i].text))
                preSpaceCount += (len(token.text) + 1)
        currentTokenIndex += 1
   
    print(lineString)
    #print str(preSpaceCount)
    carrotString = (" " * preSpaceCount)
    carrotString += ("^" * len(tokenList[i].text))
    print(carrotString)
    print("*** syntax error")
    sys.exit()





