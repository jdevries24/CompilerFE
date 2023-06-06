from Front.symbolTable import *

class SymanticError(Exception):

    def __init__(self,message,loc):
        self.message = "Symantic error at " + str(loc) + " " + message
        self.loc = loc

    def __str__(self):
        return 

class symanticCheck:

    def __init__(self):
        self.nodeFuncs = self.initCodeLookup()
        self.loopDepth = 0
        self.workingType = None
        self.symbolTable = symbolTable()
        self.nodeTable = self.initCodeLookup()
        self.inFunc = False

    def v_node(self,node):
        if node == None:
            return
        if type(node) == str:
            print(node)
            return
        return self.nodeTable[node.nodeName](node)

    def checkType(self,type):
        return self.workingType.name == type.name




    def run(self,node):
        self.v_node(node)

    def v_Assignment(self,node):
        raise NotImplementedError

    def v_Alignas(self,node):
        raise NotImplementedError

    def v_BinOp(self,node):
        raise NotImplementedError

    def v_Break(self,node):
        raise NotImplementedError

    def v_Case(self,node):
        raise NotImplementedError

    def v_Cast(self,node):
        raise NotImplementedError

    def v_Constant(self,node):
        raise NotImplementedError

    def v_Body(self,node):
        for n in node.exprs:
            self.workingType = None
            self.v_node(n)

    def v_Continue(self,node):
        raise NotImplementedError

    def v_Decl(self,node):
        scope = "Block" if self.inFunc else "Global"
        self.symbolTable.addSymbol(symbol(node.type,node.name,scope))
        self.workingType = node.type
        self.v_node(node.init)

    def v_Default(self,node):
        raise NotImplementedError

    def v_DoWhile(self,node):
        raise NotImplementedError

    def v_EllipsParm(self,node):
        raise NotImplementedError

    def v_For(self,node):
        raise NotImplementedError

    def v_FuncCall(self,node):
        raise NotImplementedError

    def v_FuncDef(self,node):
        fname = node.name
        self.symbolTable.addSymbol(symbol(node.type),fname,"Global")
        self.inFunc = True
        self.symbolTable.pushScope()
        self.v_node(node.args)
        self.v_node(node.body)
        self.symbolTable.popScope()
        self.inFunc = False

    def v_Goto(self,node):
        raise NotImplementedError

    def v_ID(self,node):
        return node.name

    def v_InitList(self,node):
        raise NotImplementedError

    def v_NamedInit(self,node):
        raise NotImplementedError

    def v_IfNode(self,node):
        raise NotImplementedError

    def v_Label(self,node):
        raise NotImplementedError

    def v_Return(self,node):
        raise NotImplementedError

    def v_StructRef(self,node):
        raise NotImplementedError

    def v_Switch(self,node):
        raise NotImplementedError

    def v_TernaryOp(self,node):
        raise NotImplementedError

    def v_UnaryOp(self,node):
        raise NotImplementedError

    def v_While(self,node):
        raise NotImplementedError

    def initCodeLookup(self):
        return {            "Assignment":self.v_Assignment,
            "Alignas":self.v_Alignas,
            "BinOp":self.v_BinOp,
            "Break":self.v_Break,
            "Case":self.v_Case,
            "Cast":self.v_Cast,
            "Constant":self.v_Constant,
            "Body":self.v_Body,
            "Continue":self.v_Continue,
            "Decl":self.v_Decl,
            "Default":self.v_Default,
            "DoWhile":self.v_DoWhile,
            "EllipsParm":self.v_EllipsParm,
            "For":self.v_For,
            "FuncCall":self.v_FuncCall,
            "FuncDef":self.v_FuncDef,
            "Goto":self.v_Goto,
            "ID":self.v_ID,
            "InitList":self.v_InitList,
            "NamedInit":self.v_NamedInit,
            "IfNode":self.v_IfNode,
            "Label":self.v_Label,
            "Return":self.v_Return,
            "StructRef":self.v_StructRef,
            "Switch":self.v_Switch,
            "TernaryOp":self.v_TernaryOp,
            "UnaryOp":self.v_UnaryOp,
            "While":self.v_While}