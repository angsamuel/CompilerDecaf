

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
    
    def __init__(self):
        self.variableDecls = []
        self.stmts = []

    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "StmtBlock:")
        for vd in self.variableDecls:
           vd.printMyStuff(tabs+1)
        
        for st in self.stmts:
            st.printMyStuff(tabs+1)


class VariableDeclClass(IRObject):
    variableClass = VariableClass()
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "VarDecl:")
    	self.variableClass.printMyStuff(tabs+1)

class FunctionDeclClass(IRObject):
    name = ""
    typeClass = TypeClass()
    ident = IdentClass()
    
    stmtBlock = StmtBlockClass()

    def __init__(self):
        self.formalsList = [] #list of variables

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

class IfStmtClass(StmtClass):
    thenStmt = StmtClass()
    elseStmt = StmtClass()
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "IfStmt:")
        print(self.mtabs(tabs+1) + "(test)")
        self.expr.printMyStuff(tabs+1)
        if self.thenStmt.finished:
            print(self.mtabs(tabs+1) + "(then)")
            self.thenStmt.printMyStuff(tabs+1)
        if self.elseStmt.finished:
            print(self.mtabs(tabs+1) + "(else)")
            self.elseStmt.printMyStuff(tabs+1)

class WhileStmtClass(StmtClass):
    bodyStmt = StmtClass()
    def printMyStuff(self, tabs):
        print(self.mtabs(tabs)+"WhileStmt:")
        print(self.mtabs(tabs+1) + "(test)")
        self.expr.printMyStuff(tabs+1)
        print(self.mtabs(tabs+1)+"(body)")
        self.bodyStmt.printMyStuff(tabs+1)


class BreakStmtClass(StmtClass):
    def printMyStuff(self,tabs):
        print self.mtabs(tabs) + "BreakStmt:"

class ReturnStmtClass(StmtClass):
    def printMyStuff(self,tabs):
        print self.mtabs(tabs) + "ReturnStmt:"
        if self.expr.finished:
            self.expr.printMyStuff(tabs+1)
        else:
            print self.mtabs(tabs+1) + "Empty:"

class PrintStmtClass(StmtClass):
    def __init__(self):
        self.exprs = []
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs)+"PrintStmt:")
        for expr in self.exprs:
            print(self.mtabs(tabs+1) + "(args)")
            expr.printMyStuff(tabs+1)

class ForStmtClass(StmtClass):
    leftExpr = ExprClass()
    midExpr = ExprClass()
    rightExpr = ExprClass()
    stmt = StmtClass()
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + "PrintStmt:")
        
        print(self.mtabs(tabs+1) + "(init)")
        if self.leftExpr.finished:
            self.leftExpr.printMyStuff(tabs+1)
        else:
            print(self.mtabs(tabs+1) + "Empty:")

        print(self.mtabs(tabs+1) + "(test)")
        self.midExpr.printMyStuff(tabs+1)

        print(self.mtabs(tabs+1) + "(step)")
        if self.rightExpr.finished:
            self.rightExpr.printMyStuff(tabs+1)
        else:
            print(self.mtabs(tabs+1) + "Empty:")

        print(self.mtabs(tabs+1) + "(body)")
        self.stmt.printMyStuff(tabs+1)






class ExprTree():
    root = None #ExprClass()
    nicoRobin = None #our active slot




class ConstantClass(IRObject):
    name = ""
    constantType = ""
    def printMyStuff(self,tabs):
        print(self.mtabs(tabs) + self.constantType + ": " + self.name)













