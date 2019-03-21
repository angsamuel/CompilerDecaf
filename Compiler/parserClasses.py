class IRObject:
    finished = False
    errorLine = -1
    errorTokenNum = -1
    def mtabs(self, tabs):
        return ("    "*tabs)
    def printMyStuff(self, tabs):
    	print("PRINTING FROM IR OBJECT")

class IdentClass(IRObject):
    name = ""
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "Identifier: " + self.name)

class TypeClass(IRObject):
    name = ""
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "Type: " + self.name)

class VariableClass(IRObject):
    typeClass = TypeClass()
    identClass = IdentClass()
    def printMyStuff(self,tabs):
    	self.typeClass.printMyStuff(tabs)
    	self.identClass.printMyStuff(tabs)

class StmtClass(IRObject):
    name = ""

class StmtBlockClass(IRObject):
    name = ""
    variableDecls = []
    stmts = []


class VariableDeclClass(IRObject):
    variableClass = VariableClass()
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "VarDecl:")
    	self.variableClass.printMyStuff(tabs+1)

class FunctionDeclClass(IRObject):
    name = ""
    typeClass = TypeClass()
    ident = IdentClass()
    formalsList = [] #list of variables
    stmtBlock = StmtBlockClass()
    print("FORMALS: ")
    print(len(formalsList))
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "FuncDecl:")
        print(self.mtabs(tabs+1) + "(return type)" + " Type: " + self.typeClass.name)
        for parameter in self.formalsList:
            print(self.mtabs(tabs+1) + "(formals)" + " VarDecl:")
            parameter.printMyStuff(tabs+2)
        print(self.mtabs(tabs+1) + "(body)" + " StmtBlock:" + str(len(self.stmtBlock.variableDecls)))
        for varDecl in self.stmtBlock.variableDecls:
            varDecl.printMyStuff(tabs+2)






