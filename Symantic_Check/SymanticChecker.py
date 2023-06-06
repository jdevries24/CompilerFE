from Symantic_Check.Jsyms import symbolTable,jsym



class Symantic_Checker:

    def __init__(self,root):
        self.root = root
        self.st = symbolTable()
        self.currentType = None
        self.ReturnType = []
        self.FuncLabels = []
        self.fordepth = 0
        self.errors = []

    def run(self):
        self.v_Node(self.root)
        for er in self.errors:
            print(er)

    def checktype(self,checktype):
        if self.currentType is None:
            self.currentType = checktype
            return True
        else:
            if self.currentType == checktype:
                return True
            self.errors.append("Type Missmatch " + str(self.currentType) + " and " + str(checktype))
            return False

    def v_Assignemnt(self,node):
        raise NotImplementedError
    
    def v_ArrayRef(self,node):
        raise NotImplementedError
    
    def v_Alignas(self,node):
        raise NotImplementedError
    
    def v_BinOp(self,node):
        return self.v_Node(node.left) and self.v_Node(node.right)
    
    def v_Break(self,node):
        raise NotImplementedError
    
    def v_Case(self,node):
        raise NotImplementedError
    
    def v_Cast(self,node):
        raise NotImplementedError
    
    def v_Constant(self,node):
        raise NotImplementedError
    
    def v_Body(self,node):
        for expr in node.exprs:
            self.currentType = None
            self.v_Node(expr)
    
    def v_Continue(self,node):
        raise NotImplementedError
    
    def v_Decl(self,node):
        self.st.addSymbol(jsym(node.name,node.type))
        return self.checktype(node.type) and self.v_Node(node.init)
    
    def v_Default(self,node):
        raise NotImplementedError
    
    def v_DoWhile(self,node):
        raise NotImplementedError
    
    def v_EllipsParm(self,node):
        pass

    def v_For(self,node):
        raise NotImplementedError
    
    def v_FuncCall(self,node):
        raise NotImplementedError
    
    def v_FuncDef(self,node):
        self.st.addSymbol(jsym(node.name,node.type))
        self.st.pushScope()
        if (node.type.qual == "base") and (node.type.name == "void"):
            self.ReturnType.append(None)
        else:
            self.ReturnType.append(node.type.rtype)
        for arg in node.args:
            self.currentType = None
            self.v_Node(arg)
        for stmt in node.body:
            self.currentType = None
            self.v_Node(stmt)
        
    
    def v_Goto(self,node):
        raise NotImplementedError
    
    def v_ID(self,node):
        ID_type = self.st.searchSymbols(node.name)
        if ID_type is None:
            self.errors.append("Cannot find "+node.name)
            return False
        else:
            return self.checktype(ID_type.stype)
    
    def v_InitList(self,node):
        raise NotImplementedError
    
    def v_NamedInit(self,node):
        raise NotImplementedError
    
    def v_IfNode(self,node):
        raise NotImplementedError
    
    def v_Label(self,node):
        raise NotImplementedError
    
    def v_Return(self,node):
        if node.expr is None:
            if self.ReturnType[-1] is None:
                return True
            else:
                self.errors.append("Expected return value")
                return False
        else:
            return self.v_Node(node.expr) and self.checktype(self.ReturnType[-1])
    
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
    
    def v_Node(self,node):
        if node is None:
            return True 
        lookup = {
            "Assignment":self.v_Assignemnt,"ArrayRef":self.v_ArrayRef,"Alignas":self.v_Alignas,
            "BinOp":self.v_BinOp,"Break":self.v_Break,"Case":self.v_Case,"Cast":self.v_Cast,"Constant":self.v_Constant,
            "Body":self.v_Body,"Continue":self.v_Continue,"Decl":self.v_Decl,"Default":self.v_Default,"DoWhile":self.v_DoWhile,
            "EllipsParm":self.v_EllipsParm,"For":self.v_For,"FuncCall":self.v_FuncCall,"FuncDef":self.v_FuncDef,"Goto":self.v_Goto,
            "ID":self.v_ID,"InitList":self.v_InitList,"NamedInit":self.v_NamedInit,"IfNode":self.v_IfNode,"Label":self.v_Label,
            "Return":self.v_Return,"StructRef":self.v_StructRef,"Switch":self.v_Switch,"TernaryOp":self.v_TernaryOp,"UnaryOp":self.v_UnaryOp,
            "While":self.v_While
        }
        return lookup[node.nodeName](node)