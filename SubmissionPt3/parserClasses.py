

class IRObject:
    finished = False
    errorLine = -1
    line = -1
    errorTokenNum = -1

    #type stuff cut my life into pieces this is my last resort
    isIdent = False
    isConstant = False
    isBreak = False
    isFuncDecl = False
    isVarDecl = False
    isStmtBlock = False
    isExpr = False
    isStmt = False
    isCall = False
    isPrint = False
    isReadInt = False
    isReadLine = False
    def mtabs(self, tabs):
        return ("    "*tabs)
    def printMyStuff(self,prefix, tabs):
    	print("PRINTING FROM IR OBJECT")


class IdentClass(IRObject):
    name = ""
    isIdent = True
    def printMyStuff(self,prefix,tabs):
        print(self.mtabs(tabs) + prefix + "Identifier: " + self.name)

class TypeClass(IRObject):
    name = ""
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix + "Type: " + self.name)

class VariableClass(IRObject):
    typeClass = TypeClass()
    identClass = IdentClass()
    def printMyStuff(self,prefix,tabs):
    	self.typeClass.printMyStuff(prefix, tabs)
    	self.identClass.printMyStuff("", tabs)

 
class StmtBlockClass(IRObject):
    name = ""
    isStmtBlock = True
    def __init__(self):
        self.variableDecls = []
        self.stmts = []

    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix + "StmtBlock:")
        for vd in self.variableDecls:
           vd.printMyStuff("",tabs+1)
        
        for st in self.stmts:
            st.printMyStuff("",tabs+1)


class VariableDeclClass(IRObject):
    variableClass = VariableClass()
    isVarDecl = True
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix + "VarDecl:")
    	self.variableClass.printMyStuff("",tabs+1)

class FunctionDeclClass(IRObject):
    isFuncDecl = True
    name = ""
    typeClass = TypeClass()
    identClass = IdentClass()
    
    stmtBlock = StmtBlockClass()

    def __init__(self):
        self.formalsList = [] #list of variables

    def printMyStuff(self,prefix, tabs):
        
        print(self.mtabs(tabs) + prefix + "FnDecl:")
        print(self.mtabs(tabs+1) + "(return type)" + " Type: " + self.typeClass.name)
        self.identClass.printMyStuff("",tabs+1)

        for parameter in self.formalsList:
            print(self.mtabs(tabs+1) + "(formals)" + " VarDecl:")
            parameter.printMyStuff("",tabs+2)
        
        print(self.mtabs(tabs+1) + "(body)" + " StmtBlock:")

        for varDecl in self.stmtBlock.variableDecls:
            varDecl.printMyStuff("",tabs+2)
        for stmt in self.stmtBlock.stmts:
            stmt.printMyStuff("", tabs+2)

class ExprClass(IRObject):
    name = ""
    operator = ""
    parent = None
    leftChild = None
    rightChild = None
    isExpr = True
    score = 0
    def printMyStuff(self, prefix, tabs):
        exprTypeString = prefix
        if self.operator in ["="]:
            exprTypeString += "AssignExpr:"
        elif self.operator in ["+","-","*","/", "%"]:
            exprTypeString += "ArithmeticExpr:"
        elif self.operator in ["==", "!="]:
            exprTypeString += "EqualityExpr:"
        elif self.operator in [">","<",">=","<="]:
            exprTypeString += "RelationalExpr:"
        elif self.operator in ["&&", "||", "!"]:
            exprTypeString += "LogicalExpr:"

        
        print(self.mtabs(tabs) + exprTypeString)

        if self.leftChild != None:
            if self.leftChild.isIdent:
                print(self.mtabs(tabs+1) + "FieldAccess:")
                self.leftChild.printMyStuff("",tabs+2)
            else:
                self.leftChild.printMyStuff("",tabs+1)
        
        if self.operator != "":
            print(self.mtabs(tabs+1) + "Operator: " + self.operator) 
        
        if self.rightChild != None:
            if self.rightChild.isIdent:
                print(self.mtabs(tabs+1) + "FieldAccess:")
                self.rightChild.printMyStuff("",tabs+2)
            else:
                self.rightChild.printMyStuff("",tabs+1)



class StmtClass(IRObject):
    name = ""
    expr = ExprClass()
    isStmt = True
    stmtType = ""
    def printMyStuff(self,prefix, tabs):
        if self.expr == None:
            print(self.mtabs(tabs) + prefix + "Empty:")
        elif self.expr.isIdent:
            print(self.mtabs(tabs) +prefix + "FieldAccess:")
            self.expr.printMyStuff("",tabs+1)
        else:
            self.expr.printMyStuff(prefix, tabs)

class IfStmtClass(StmtClass):
    thenStmt = StmtClass()
    elseStmt = StmtClass()
    stmtType = "if"
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix + "IfStmt:")
        self.expr.printMyStuff("(test)", tabs+1)
        if self.thenStmt.finished:
            self.thenStmt.printMyStuff("(then)", tabs+1)
        if self.elseStmt.finished:
            self.elseStmt.printMyStuff("(else)", tabs+1)

class WhileStmtClass(StmtClass):
    stmt = StmtClass()
    stmtType = "while"
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs)+prefix + "WhileStmt:")
        self.expr.printMyStuff("(test)",tabs+1)
        self.bodyStmt.printMyStuff("(body)", tabs+1)


class BreakStmtClass(StmtClass):
    isBreak = True
    def printMyStuff(self,prefix,tabs):
        print self.mtabs(tabs) + prefix +  "BreakStmt:"

class ReturnStmtClass(StmtClass):
    stmtType = "return"
    def printMyStuff(self,prefix, tabs):
        print self.mtabs(tabs) + prefix + "ReturnStmt:"
        if self.expr.finished:
            self.expr.printMyStuff("",tabs+1)
        else:
            print self.mtabs(tabs+1) + "Empty:"

class PrintStmtClass(StmtClass):
    isPrint = True
    def __init__(self):
        self.exprs = []
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs)+prefix+"PrintStmt:")
        for expr in self.exprs:
            if expr.isIdent:
                print(self.mtabs(tabs+1) + "(args)" + "FieldAccess:")
                expr.printMyStuff("",tabs+2)
            else:
                expr.printMyStuff("(args)",tabs+1)

class ForStmtClass(StmtClass):
    leftExpr = ExprClass()
    midExpr = ExprClass()
    rightExpr = ExprClass()
    stmt = StmtClass()
    stmtType = "for"
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix +  "ForStmt:")
        
        if self.leftExpr.finished:
            self.leftExpr.printMyStuff("(init)", tabs+1)
        else:
            print(self.mtabs(tabs+1) + "(init)" +  "Empty:")

        self.midExpr.printMyStuff("(test)", tabs+1)

        if self.rightExpr.finished:
            self.rightExpr.printMyStuff("(step)",tabs+1)
        else:
            print(self.mtabs(tabs+1) + prefix +  "Empty:")

        self.stmt.printMyStuff("(body)",tabs+1)






class ExprTree():
    root = None #ExprClass()
    nicoRobin = None #our active slot




class ConstantClass(IRObject):
    name = ""
    constantType = ""
    isConstant = True
    def printMyStuff(self,prefix, tabs):
        if "Double" in self.constantType:
            if "." in self.name and self.name.split(".")[1] == "0":
                self.name = self.name.split(".")[0]
        print(self.mtabs(tabs) + prefix+ self.constantType + ": " + self.name)




class CallClass(IRObject):
    isCall = True
    identClass = IdentClass()
    def __init__(self):
        self.actuals = []
    def printMyStuff(self,prefix,tabs):
        print(self.mtabs(tabs) + prefix + "Call:")
        self.identClass.printMyStuff("",tabs+1)
        for actual in self.actuals:
            if actual.isIdent:
                print(self.mtabs(tabs+1) + "(actuals) FieldAccess:")
                actual.printMyStuff("", tabs+2)
            else:
                actual.printMyStuff("(actuals) ", tabs+1)

class ReadIntegerClass(IRObject):
    name = ""
    isReadInt = True
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix + "ReadIntegerExpr:")

class ReadLineClass(IRObject):
    name = ""
    isReadLine = True
    def printMyStuff(self,prefix, tabs):
        print(self.mtabs(tabs) + prefix +"ReadLineExpr:")








