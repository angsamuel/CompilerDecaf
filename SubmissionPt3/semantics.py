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



#questions
#can parameters be duplicates?


#just for breaks
loopLevel = 0
ifCount = 0
elseCount = 0
loopCount = 0

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
	fileContents = fc

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


def printExprOperandError(irOb, line, leftType, rightType, operator):
	global fileContents
	print("*** Error line " + str(line) + ".")
	print(fileContents.split("\n")[line-1])
	print("^")
	print("*** Incompatible operands: " + leftType + " " + operator + " " + rightType)
	print ""


def printDupeIdentError(irOb):
	global fileContents
	print("*** Error line " + str(irOb.line) + ".")
	print(fileContents.split("\n")[irOb.line-1])
	print("^" * len(irOb.identClass.name))
	print("Duplicate declaration of variable/function " + irOb.identClass.name)
	print ""



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
		if stmt.bodyStmt.isStmtBlock:
			loopCount += 1
			currentScope.append("LOOP" + str(loopCount))
			checkStmtForVarDecls(stmt)
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

	matchedType = "YIKES"


	for i in range(0,len(varNames)):
		if varNames[i] == v.name:
			if len(varScopes[i]) <= len(currentScope): #we could access this
				scopeMatches = True
				for j in range(0,len(varScopes[i])):
					if varScopes[i][j] != currentScope[j]:
						scopeMatches = False
				if scopeMatches:
					matchedType = varTypes[i]
	return matchedType
					#we have a possible match







arithOps = ["*","-","+","/", "%"]
boolOps = [">", "<", ">=", "<=", "=="]
exprSuperLine = -1


def convertConstType(typeString):
	return typeString.replace("Constant","").lower()

def verifyExpr(expr):
	global arithOps
	global currentScope
	global exprSuperLine
	returnValue = "error"

	clearSuperLineAfter = False
	if exprSuperLine == -1:
		clearSuperLineAfter = True
		exprSuperLine = expr.line

	if expr.isIdent:
		returnValue = identTypeInScope(expr)
	elif expr.isConstant:
		returnValue = expr.constantType
	elif expr.operator in arithOps:
		rightType = convertConstType(verifyExpr(expr.rightChild))
		leftType = convertConstType(verifyExpr(expr.leftChild))
		if rightType != leftType:
			printExprOperandError(expr, exprSuperLine, leftType, rightType, expr.operator)
			returnValue = "error"
		else:
			returnValue = rightType
	elif expr.operator == "=":
		rightType = convertConstType(verifyExpr(expr.rightChild))
		if expr.leftChild.isIdent:
			if identTypeInScope(expr.leftChild) == rightType:
				returnValue = "assignment"
			else:
				if rightType != "error":
					printExprOperandError(expr, exprSuperLine, identTypeInScope(expr.leftChild), rightType, expr.operator)
				returnValue = "error"

	if clearSuperLineAfter:
		exprSuperLine = -1
	return returnValue

	#if we have a problem, return the type


def verifyStmt(stmt):
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








