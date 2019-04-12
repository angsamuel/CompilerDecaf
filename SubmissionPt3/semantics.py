#layout of program
#first gather all declarations, check for duplicates


#order to do these things in

#(in order)
#-line number tracking - probably working
#-variable and function duplication is not allowed - function dupe is done
#-break statements only appear in loops
#-functions take correct number of arguments

#-variables declared in same or greater scope
#-operators use correct types
#-functions take correct type of arguments

#scope naming - global, function name, 


#questions
#can parameters be duplicates?


#just for breaks
loopLevel = 0

funcTypes = []
funcParameters = [] #2d array of types
funcNames = []

varNames = []
varScopes = []
varTypes = []

currentScope = ["GLOBAL"]

fileContents = ""


def check(ir, fc):
	global fileContents
	fileContents = fc
	grabAllDecls(ir)


def grabAllDecls(ir):
	global funcParameters
	global funcNames
	global funcTypes
	for irOb in ir:
		if irOb.isFuncDecl:
			#add the name
			if (irOb.identClass.name) in funcNames:
				printDupeFuncError(irOb)

			funcNames.append(irOb.identClass.name)
			funcTypes.append(irOb.typeClass.name)
			tempFuncParameters = []

			#we're now inside the scope of this function
			currentScope.append(irOb.identClass.name + "PARAMETERS")
			

			for f in irOb.formalsList:
				tempFuncParameters.append(f.typeClass.name)
				packageVarDecl(f)


			funcParameters.append(tempFuncParameters)

			currentScope.append(irOb.identClass.name + "BODY")

			#once we have the function itself, we will later need to 
			#dig through and grab all the vardeclstoo

			#leaving scope of the function

			currentScope.pop() #pop parameters
			currentScope.pop() #pop body
		else:
			packageVarDecl(irOb)


def grabAllVarDecls(ir):
	a = 1


def printDupeIdentError(irOb):
	global fileContents
	print("*** Error line " + str(irOb.line) + ".")
	print(fileContents.split("\n")[irOb.line-1])
	print("^" * len(irOb.identClass.name))
	print("Duplicate identifier in same scope.")


def packageVarDecl(v):
	global funcNames
	global varNames
	global varTypes
	global varScopes
	global currentScope
	
	foundDupe = False

	#check for dupes in var names
	for i in range(0,len(varNames)):
		if  not foundDupe and varNames[i] == v.identClass.name:
			if varScopes[i] == currentScope:
				printDupeIdentError(v.variableClass)
				foundDupe = True

	#check for dupes in function names
	for i in range(0, len(funcNames)):
		if not foundDupe and funcNames[i] == v.variableClass.identClass.name:
			if currentScope == ["GLOBAL"]:
				printDupeIdentError(v.variableClass)
				foundDupe = True


	varNames.append(v.variableClass.identClass.name)
	varTypes.append(v.variableClass.typeClass.name)
	varScopes.append(currentScope)




