from parserClasses import *

#layout of program
#first gather all declarations, check for duplicates


#order to do these things in

#(in order)
#-line number tracking - probably working
#-variable and function duplication is not allowed - function dupe is done, variable dupe is done
#-break statements only appear in loops
#-functions take correct number of arguments

#-used variables are declared in same or greater scope
#-operators use correct types
#-functions take correct type of arguments

#WHAT IS LEFT TO DO
#Prints -E
#ReadLines -E
#error carrot matching -H
#edge case stuff that I probably don't need to do -kms
#final testing


#questions
#can parameters be duplicates?


#just for breaks
loopLevel = 0
ifCount = 0
elseCount = 0
loopCount = 0

loopLevel = 0

funcTypes = []
funcParameters = [] #2d array of types
funcNames = []
funcVerified = []
funcDeclSpottedDict = {}

varNames = []
varScopes = []
varTypes = []
varVerified = []

currentScope = ["GLOBAL"]

fileContents = ""




def appendVarScope():
	global currentScope
	global varScopes
	tempScope = []
	for s in currentScope:
		tempScope.append(s)
	varScopes.append(tempScope)


def check(ir, fc):
	global fileContents
	global ifCount
	global elseCount
	global loopCount
	fileContents = fc

	ifCount = 0
	elseCount = 0
	loopCount = 0

	#first grab all the declarations
	grabAllDecls(ir)
	funcDeclSpottedDict.clear()
	#we don't need to check for duplicates
	verifyAST(ir)



	#print(varNames)
	#print(varScopes)


def grabAllDecls(ir):
	global funcParameters
	global funcNames
	global funcTypes
	global funcVerified
	global funcDeclSpottedDict

	for irOb in ir:
		if irOb.isFuncDecl:
			#add the name
			#if (irOb.identClass.name) in funcNames:
				#printDupeFuncError(irOb)

			funcNames.append(irOb.identClass.name)
			funcTypes.append(irOb.typeClass.name)
			funcVerified.append(False)

			tempFuncParameters = []


			if irOb.identClass.name in funcDeclSpottedDict:
				funcDeclSpottedDict[irOb.identClass.name] = funcDeclSpottedDict[irOb.identClass.name] + 1
			else:
				funcDeclSpottedDict[irOb.identClass.name] = 1

			#we're now inside the scope of this function
			currentScope.append(irOb.identClass.name + "PARAMETERS" + str(funcDeclSpottedDict[irOb.identClass.name]))
			

			for f in irOb.formalsList:
				tempFuncParameters.append(f.typeClass.name)
				packageVarDecl(f)


			funcParameters.append(tempFuncParameters)

			currentScope.append(irOb.identClass.name + "BODY" + str(funcDeclSpottedDict[irOb.identClass.name]))

			#once we have the function itself, we will later need to 
			#dig through and grab all the vardeclstoo
			#check
			checkStmtBlockForVarDecls(irOb.stmtBlock)

			#leaving scope of the function

			currentScope.pop() #pop parameters
			currentScope.pop() #pop body
		else:
			packageVarDecl(irOb)


def getParameterString(lineString, paramIndex):
	subStart = 0
	subEnd = 0

	currentParam = -1
	rightsNeeded = 0

	foundGuts = False
	foundRightParam = False
	index = 0

	for c in lineString:
		if c == '(':
			if not foundGuts:
				foundGuts = True
				currentParam += 1
			else:
				rightsNeeded += 1
		elif c == ')':
			if rightsNeeded < 1:
				subEnd = index
				break #we're done 
			else:
				rightsNeeded -= 1			
		elif c == ',':
			if rightsNeeded < 1:
				currentParam += 1
				if foundRightParam:
					subEnd = index
					break

		if currentParam == paramIndex and not foundRightParam:
			foundRightParam = True
			subStart = index + 1
		
		index += 1

	return lineString[subStart:subEnd].strip()

def getTestString(lineString):

	if "for" in lineString:
		return lineString.split(";")[1].strip()
	else:
		return getParameterString(lineString,0)



def printExprOperandError(irOb, line, leftType, rightType, operator):
	global fileContents
	print""
	print("*** Error line " + str(line) + ".")
	print(fileContents.split("\n")[line-1])
	print("^" * len(irOb.operator))
	if leftType == "":
		print("*** Incompatible operand: " + leftType + " " + operator + " " + rightType)
	else:
		print("*** Incompatible operands: " + leftType + " " + operator + " " + rightType)
	print ""

def printDupeIdentError(irOb):
	global fileContents
	print""
	print("*** Error line " + str(irOb.line) + ".")
	print(fileContents.split("\n")[irOb.line-1])
	print("^" * len(irOb.identClass.name))
	print("Duplicate declaration of variable/function " + irOb.identClass.name)
	print ""

def printBadTestExpr(exprOb):
	global fileContents
	print""
	print("*** Error line " + str(exprOb.line) + ".")
	print(fileContents.split("\n")[exprOb.line-1])

	#find the number of carrots we need
	chunkWeWant = getTestString(fileContents.split("\n")[exprOb.line-1])


	print("^" * len(chunkWeWant))
	print("*** Test expression must have boolean type")
	print("")

def printBadBreakError(breakOb):
	global fileContents
	print""
	print("*** Error line " + str(breakOb.line) + ".")
	print(fileContents.split("\n")[breakOb.line-1])
	print("^^^^^")
	print("*** break is only allowed inside a loop")
	print""

def printBadReturn(returnOb, retType):
	global fileContents
	global returnTypeNeeded
	print""
	print("*** Error line " + str(returnOb.line) + ".")
	print(fileContents.split("\n")[returnOb.line-1])

	chunkWeWant = fileContents.split("\n")[returnOb.line-1].split("return")[1].split(";")[0].strip()
	print("^" * len(chunkWeWant))

	print("*** Incompatible return: " + retType + " given, " + returnTypeNeeded + " expected")
	print""

def printFuncParametersMismatchError(callOb, got, needed):
	print""
	print("*** Error line " + str(callOb.line) + ".")
	print(fileContents.split("\n")[callOb.line-1])
	print("^"*len(callOb.identClass.name))
	print("*** Function \'" + callOb.identClass.name + "\' expects " + str(needed) + " arguments but " + str(got) + " given")
	print""

def printWrongFuncParameterType(callOb, index, got, needed):
	print""
	print("*** Error line " + str(callOb.line) + ".")
	print(fileContents.split("\n")[callOb.line-1])

	chunkWeWant = getParameterString(fileContents.split("\n")[callOb.line-1], index)
	print ("^" * len(chunkWeWant))

	print("*** Incompatible argument " + str(index+1) + ": " +  got + " given, " + needed + " expected")

	print""

def printWrongPrintParamter(printOb, index, got):
	print""
	print("*** Error line " + str(printOb.line) + ".")
	print(fileContents.split("\n")[printOb.line-1])
	chunkWeWant = getParameterString(fileContents.split("\n")[printOb.line-1],index)
	print("^"*len(chunkWeWant))
	print("*** Incompatible argument " + str(index+1) + ": " + got + " given, int/bool/string expected")
	print""

def printIdentNotFoundInScope(identOb):
	print""

	print("*** Error line " + str(identOb.line) + ".")
	print(fileContents.split("\n")[identOb.line-1])
	print("^"*len(identOb.name))
	print("*** No declaration found for variable \'" + identOb.name + "\'")
	print""

	

def packageVarDecl(v):
	global funcNames
	global varNames
	global varTypes
	global varScopes
	global varVerified
	global currentScope
	
	foundDupe = False

	if not v.isVarDecl: #we have a parameter
		tempV = v
		v = VariableDeclClass()
		v.variableClass = tempV

	varNames.append(v.variableClass.identClass.name)
	varTypes.append(v.variableClass.typeClass.name)
	varVerified.append(False)
	#varScopes.append(currentScope.copy())
	appendVarScope()


def checkStmtForVarDecls(stmt):
	global currentScope
	global ifCount
	global loopCount
	global elseCount

	if stmt.stmtType == "if":
		if stmt.thenStmt.isStmtBlock:
			#we got one
			ifCount += 1
			currentScope.append("IF" + str(ifCount))
			checkStmtBlockForVarDecls(stmt.thenStmt)
			currentScope.pop()
		if stmt.elseStmt != None and stmt.elseStmt.isStmtBlock:
			elseCount += 1
			currentScope.append("ELSE" + str(elseCount))
			checkStmtBlockForVarDecls(stmt.elseStmt)
			currentScope.pop()

	if stmt.stmtType == "for" or stmt.stmtType == "while":
		if stmt.stmt.isStmtBlock:
			loopCount += 1
			currentScope.append("LOOP" + str(loopCount))
			checkStmtBlockForVarDecls(stmt.stmt)
			currentScope.pop()



def checkStmtBlockForVarDecls(stmtBlock):
	for v in stmtBlock.variableDecls:
		packageVarDecl(v)
	for s in stmtBlock.stmts:
		checkStmtForVarDecls(s)




#verification-------------------------------------------------------


returnTypeNeeded = ""

def verifyFuncDecl(funcDeclOb):
	global funcNames
	global varNames
	global varScopes
	global funcVerified
	global varVerified

	dupeFound = False
	#check through func names, if we got the same scope, 
	for i in range(0,len(funcNames)):
		if funcNames[i] == funcDeclOb.identClass.name:
			#we might have found our match
			if funcVerified[i]:
				printDupeIdentError(funcDeclOb)
				dupeFound = True
				break
			else:
				funcVerified[i] = True
				break

	if not dupeFound:
		for i in range(0, len(varNames)):
			if varNames[i] == funcDeclOb.identClass.name:
				if varVerified[i]:
					if varScopes[i] == ["GLOBAL"]:
						printDupeIdentError(funcDeclOb)



def verifyVarDecl(varDeclOb):
	global funcNames
	global varNames
	global varScopes
	global funcVerified
	global varVerified


	dupeFound = False
	#check through func names, if we got the same scope, 

	for i in range(0,len(varNames)):
		# print("COMPARE")
		# print(varScopes[i])
		# print(currentScope)
		# print("END")
		if varNames[i] == varDeclOb.variableClass.identClass.name:
			#we might have found our match
			if varVerified[i]:
				if varScopes[i] == currentScope and not dupeFound:
					printDupeIdentError(varDeclOb.variableClass)
					dupeFound = True
			else:
				varVerified[i] = True
				break

	if not dupeFound:
		for i in range(0, len(funcNames)):
			if funcNames[i] == varDeclOb.variableClass.identClass.name:
				if funcVerified[i]:
					if currentScope == ["GLOBAL"]:
						printDupeIdentError(varDeclOb.variableClass)






def identTypeInScope(v): #takes an ident
	global currentScope
	global varNames
	global varScopes
	global varTypes

	matchedType = "error"


	for i in range(0,len(varNames)):
		if varNames[i] == v.name:
			if len(varScopes[i]) <= len(currentScope): #we could access this
				scopeMatches = True
				for j in range(0,len(varScopes[i])):
					if varScopes[i][j] != currentScope[j]:
						scopeMatches = False
				if scopeMatches:
					matchedType = varTypes[i]

	
	if matchedType == "error":
		printIdentNotFoundInScope(v)

	return matchedType
					#we have a possible match







arithOps = ["*","-","+","/", "%"]
boolOps = ["&&", "||"]
compOps = ["==","!=","<",">",">=","<="]
exprSuperLine = -1


def convertConstType(typeString):
	return typeString.replace("Constant","").lower()

def verifyExpr(expr):
	global arithOps
	global boolOps
	global currentScope
	global exprSuperLine
	global compOps
	returnValue = "error"

	if expr.isCall: 
		return verifyCall(expr)
	elif expr.isReadInt:
		return "int"
	elif expr.isReadLine:
		return "string"


	clearSuperLineAfter = False
	if exprSuperLine == -1:
		clearSuperLineAfter = True
		exprSuperLine = expr.line


	if expr.isIdent:
		returnValue = identTypeInScope(expr)
	elif expr.isConstant:
		returnValue = expr.constantType
	elif expr.operator == "-" and expr.leftChild == None:
		rightType = convertConstType(verifyExpr(expr.rightChild))
		if rightType != "error" and (rightType == "bool" or rightType == "assignment" or rightType == "string"):
			printExprOperandError(expr, exprSuperLine, "", rightType, expr.operator)
			returnValue = "error"
		else:
			returnValue = rightType
	elif expr.operator in arithOps or expr.operator in compOps:
		rightType = convertConstType(verifyExpr(expr.rightChild))
		leftType = convertConstType(verifyExpr(expr.leftChild))
		if rightType != leftType:
			if rightType != "error" and leftType != "error":
				printExprOperandError(expr, exprSuperLine, leftType, rightType, expr.operator)
			returnValue = "error"
		else:
			if rightType == "error":
				returnValue = "error"
			elif rightType == "bool" or rightType == "assignment" or rightType == "string":
				printExprOperandError(expr, exprSuperLine, leftType, rightType, expr.operator)
				returnValue = "error"
			else:
				if expr.operator in compOps:
					returnValue = "bool"
				else:
					returnValue = rightType
	elif expr.operator in boolOps:
		rightType = convertConstType(verifyExpr(expr.rightChild))
		leftType = convertConstType(verifyExpr(expr.leftChild))
		if rightType != leftType:
			if rightType != "error" and leftType != "error":
				printExprOperandError(expr, exprSuperLine, leftType, rightType, expr.operator)
			returnValue = "error"
		else:
			if rightType == "error":
				returnValue = "error"
			if rightType != "bool":
				printExprOperandError(expr, exprSuperLine, leftType, rightType, expr.operator)
				returnValue = "error"
			else:
				returnValue = rightType
	elif expr.operator == "=":
		rightType = convertConstType(verifyExpr(expr.rightChild))
		if expr.leftChild.isIdent:
			vType = identTypeInScope(expr.leftChild);
			if vType == rightType:
				returnValue = "assignment"
			else:
				if rightType != "error" and vType != "error":
					printExprOperandError(expr, exprSuperLine, identTypeInScope(expr.leftChild), rightType, expr.operator)
				returnValue = "error"
	elif expr.operator == "!":
		rightType = convertConstType(verifyExpr(expr.rightChild))
		if rightType != "bool" and rightType != "error":
			printExprOperandError(expr, exprSuperLine, "", rightType, expr.operator)
			returnValue = "error"
		else:
			returnValue = rightType
	


	if clearSuperLineAfter:
		exprSuperLine = -1
	return returnValue

	#if we have a problem, return the type

def verifyIfStmt(ifStmt):
	global ifCount
	global elseCount
	global currentScope

	ifCount += 1
	currentScope.append("IF" + str(ifCount))
	exprType = convertConstType(verifyExpr(ifStmt.expr))

	if exprType != "bool" and exprType != "error":
		printBadTestExpr(ifStmt.expr)

	verifyStmt(ifStmt.thenStmt)
	
	currentScope.pop()

	if ifStmt.elseStmt.finished:
		elseCount += 1
		currentScope.append("ELSE" + str(elseCount))
		verifyStmt(ifStmt.elseStmt)
		currentScope.pop()



def verifyBreakStmt(breakOb):
	global loopLevel
	if loopLevel < 1:
		printBadBreakError(breakOb);


def verifyWhileStmt(whileStmt):
	global loopLevel
	global loopCount
	global currentScope

	loopCount += 1

	currentScope.append("LOOP" + str(loopCount))

	stmtType = convertConstType(verifyExpr(whileStmt.expr))
	if stmtType != "bool" and stmtType != "error":
		printBadTestExpr(whileStmt.expr)

	loopLevel += 1
	verifyStmt(whileStmt.stmt)
	loopLevel -= 1

	currentScope.pop()



def verifyForStmt(forStmt):
	global loopLevel
	global loopCount
	global currentScope

	loopCount += 1

	currentScope.append("LOOP" + str(loopCount))

	verifyExpr(forStmt.leftExpr)
	middleType = convertConstType(verifyExpr(forStmt.midExpr))
	if middleType != "bool" and middleType != "error":
		printBadTestExpr(forStmt.midExpr)


	verifyExpr(forStmt.rightExpr)

	loopLevel += 1
	#here we check the statement block
	verifyStmt(forStmt.stmt)

	loopLevel -= 1

	currentScope.pop()

def verifyReturnStmt(retStmt):
	global returnTypeNeeded
	returnType = convertConstType(verifyExpr(retStmt.expr))
	if returnType != returnTypeNeeded and returnType != "error":
		printBadReturn(retStmt, returnType)


def verifyPrint(printStmt):

	for i in range(0,len(printStmt.exprs)):
		expr = printStmt.exprs[i]
		typeString = convertConstType(verifyExpr(expr))
		if typeString not in ["int", "bool", "string", "error"]:
			printWrongPrintParamter(printStmt,i, typeString)




def verifyCall(callStmt):
	global funcNames
	global funcTypes
	global funcParameters
	callName = callStmt.identClass.name
	returnType = "error"

	sizeMissIndex = -1
	sizeMismatch = False


	typeMismatch = False

	possibleTypeMatches = []

	myParamTypes = []
	theOneIGot = -1

	for i in range(0,len(funcNames)):
		if funcNames[i] == callName:
			#returnType = funcTypes[i]
			#first compare the number
			if len(funcParameters[i]) != len(callStmt.actuals):
				#printFuncParametersMismatchError(callStmt, len(callStmt.actuals), len(funcParameters[i]))
				sizeMissIndex = i
				sizeMismatch = True

			else:
				#we need to make sure the types all match
				possibleTypeMatches.append(i)

		

	for j in range(0, len(callStmt.actuals)):
		exprType = convertConstType(verifyExpr(callStmt.actuals[j]))
		myParamTypes.append(exprType)
			

	gotOne = False
	for i in possibleTypeMatches:
		gotOne = True
		for j in range(0,len(myParamTypes)):
			if myParamTypes[j] != funcParameters[i][j]:
					#printWrongFuncParameterType(callStmt, j, exprType, funcParameters[i][j])
				gotOne = False
		if gotOne:
			theOneIGot = i

		#if we're here, it means one didn't match
	if not gotOne and len(possibleTypeMatches) > 0:
		for j in range(0,len(myParamTypes)):
			if myParamTypes[j] != funcParameters[possibleTypeMatches[0]][j]:
				printWrongFuncParameterType(callStmt, j, exprType, funcParameters[possibleTypeMatches[0]][j])
				#gotOne = False
	elif not gotOne and sizeMismatch:
		printFuncParametersMismatchError(callStmt, len(callStmt.actuals), len(funcParameters[sizeMissIndex]))
	elif not gotOne: #we didn't even find one
		printIdentNotFoundInScope(callStmt.identClass)

	if theOneIGot > -1:
		returnType = funcTypes[theOneIGot]

	return returnType



def verifyStmt(stmt):

	if stmt.isPrint:
		verifyPrint(stmt)
	if stmt.isStmtBlock:
		verifyAny(stmt)
	elif stmt.stmtType == "if":
		verifyIfStmt(stmt)
	elif stmt.stmtType == "while":
		verifyWhileStmt(stmt)
	elif stmt.stmtType == "for":
		verifyForStmt(stmt)
	elif stmt.stmtType == "return":
		verifyReturnStmt(stmt)
	elif stmt.isBreak:
		verifyBreakStmt(stmt)
	else:
		verifyExpr(stmt.expr)

def verifyAny(irOb):
	
	global currentScope
	global returnTypeNeeded
	global funcDeclSpottedDict

	if irOb.isFuncDecl:
		returnTypeNeeded = irOb.typeClass.name
		verifyFuncDecl(irOb)
		

		if irOb.identClass.name in funcDeclSpottedDict:
			funcDeclSpottedDict[irOb.identClass.name] = funcDeclSpottedDict[irOb.identClass.name] + 1
		else:
			funcDeclSpottedDict[irOb.identClass.name] = 1

		currentScope.append(irOb.identClass.name + "PARAMETERS" + str(funcDeclSpottedDict[irOb.identClass.name]))
		currentScope.append(irOb.identClass.name + "BODY" + str(funcDeclSpottedDict[irOb.identClass.name]))
		verifyAny(irOb.stmtBlock)
		currentScope.pop()
		currentScope.pop()
		returnTypeNeeded = ""
	elif irOb.isVarDecl:
		verifyVarDecl(irOb)
	elif irOb.isStmtBlock:

		for varDecl in irOb.variableDecls:
			verifyVarDecl(varDecl)
		for stmt in irOb.stmts:
			verifyStmt(stmt)


	#evaluate expression

	#evaluate loop

	#evaluate if

	#evaluate calls



def verifyAST(ir):
	global currentScope
	global varScopes
	global varNames
	currentScope = ["GLOBAL"]
	for irOb in ir:
		verifyAny(irOb)
	#print varScopes
	#print varNames








