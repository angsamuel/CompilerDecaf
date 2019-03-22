

class IRObject:
    finished = False
    errorLine = -1
    errorTokenNum = -1
    isIdent = False
    def mtabs(self, tabs):
        return ("    "*tabs)
    def printMyStuff(self, tabs):
    	print("PRINTING FROM IR OBJECT")

class IdentClass(IRObject):
    name = ""
    isIdent = True
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
    def printMyStuff(self,tabs):
        
        print(self.mtabs(tabs) + "FuncDecl:")
        print(self.mtabs(tabs+1) + "(return type)" + " Type: " + self.typeClass.name)
        self.ident.printMyStuff(tabs+1)

        for parameter in self.formalsList:
            print(self.mtabs(tabs+1) + "(formals)" + " VarDecl:")
            parameter.printMyStuff(tabs+2)
        
        print(self.mtabs(tabs+1) + "(body)" + " StmtBlock:")

        for varDecl in self.stmtBlock.variableDecls:
            varDecl.printMyStuff(tabs+2)
        for stmt in self.stmtBlock.stmts:
            stmt.printMyStuff(tabs+2)

class ExprClass(IRObject):
    name = ""
    operator = ""
    parent = None
    leftChild = None
    rightChild = None
    def printMyStuff(self, tabs):
        exprTypeString = ""
        if self.operator in ["="]:
            exprTypeString = "AssignExpr:"
        elif self.operator in ["+","-","*","/"]:
            exprTypeString = "ArithmeticExpr:"
        
        print(self.mtabs(tabs) + exprTypeString)

        if self.leftChild != None:
            if self.leftChild.isIdent:
                print(self.mtabs(tabs+1) + "FieldAccess:")
                self.leftChild.printMyStuff(tabs+2)
            else:
                self.leftChild.printMyStuff(tabs+1)
        
        if self.operator != "":
            print(self.mtabs(tabs+1) + "Operator: " + self.operator) 
        
        if self.rightChild != None:
            if self.rightChild.isIdent:
                print(self.mtabs(tabs+1) + "FieldAccess:")
                self.rightChild.printMyStuff(tabs+2)
            else:
                self.rightChild.printMyStuff(tabs+1)



class StmtClass(IRObject):
    name = ""
    expr = ExprClass()
    def printMyStuff(self,tabs):
        self.expr.printMyStuff(tabs)

class ExprTree():
    root = None #ExprClass()
    nicoRobin = None #our active slot




class ConstantClass(IRObject):
    name = ""
    constantType = ""










