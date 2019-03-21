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


class VariableDeclClass(IRObject):
    variableClass = VariableClass()
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "VarDecl:")
    	self.variableClass.printMyStuff(tabs+1)

class FunctionDeclClass(IRObject):
    name = ""
