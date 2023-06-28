class SymanticError(Exception):

    def __init__(self,message,cords):
        self.message = message
        self.line = cords.line
        self.col = cords.column
        self.file = cords.file

class Symantic_Checker:

    def __init__(self):
        self.SymbolStack = [{}]
        self.currentType = None
        self.returnType = None
        self.fordepth = 0
        self.errors = []
        self.lookup = {
            "Assignment":self.v_Assignemnt,"ArrayRef":self.v_ArrayRef,"Alignas":self.v_Alignas,
            "BinOp":self.v_BinOp,"Break":self.v_Break,"Case":self.v_Case,"Cast":self.v_Cast,"Constant":self.v_Constant,
            "Body":self.v_Body,"Continue":self.v_Continue,"Decl":self.v_Decl,"Default":self.v_Default,"DoWhile":self.v_DoWhile,
            "EllipsParm":self.v_EllipsParm,"For":self.v_For,"FuncCall":self.v_FuncCall,"FuncDef":self.v_FuncDef,"Goto":self.v_Goto,
            "ID":self.v_ID,"InitList":self.v_InitList,"NamedInit":self.v_NamedInit,"IfNode":self.v_IfNode,"Label":self.v_Label,
            "Return":self.v_Return,"StructRef":self.v_StructRef,"Switch":self.v_Switch,"TernaryOp":self.v_TernaryOp,"UnaryOp":self.v_UnaryOp,
            "While":self.v_While
        }

    def getSymbol(self,symbolName,node):
        for dic in self.SymbolStack:
            if symbolName in dic:
                return dic[symbolName]
        raise SymanticError("Cannot find symbol "+symbolName,node.cords)
    
    def addSymbol(self,symbolName,propertys,node):
        for dic in self.SymbolStack:
            if symbolName in dic:
                raise SymanticError("Symbol "+symbolName+"All ready defined",node.cords)
        self.SymbolStack[-1].update({symbolName:propertys})

    def run(self,root):
        self.v_Node(root)
        return self.errors

    def checktype(self,checktype,node):
        if self.currentType is None:
            self.currentType = checktype
            return True
        else:
            if str(self.currentType) == str(checktype):
                return True
            if node != None:
                raise SymanticError("Missmatched types "+str(self.currentType)+","+str(checktype),node.cords)
            return False
        
    def checkconst(self,consttype,node):
        if self.currentType is None:
            return True
        if consttype == "int":
            if not self.checkIsInt(self.currentType) and node is not None:
                raise SymanticError(str(self.currentType) + "is Not a interger",node.cords)
            
    def getbase(self,property):
        while(property.qual == "syth"):
            property = property.rtype
        return property
    
    def checkIsInt(self,property):
        property = self.getbase(property)
        if str(property) in ["unsigned char","unsigned short","unsigned int","unsigned long","unsigned long long","char","short","int","long","long long"]:
            return True
        if (property.qual == "ptr"):
            return True
        else:
            return False
        
            
    def v_ExprList(self,explist):
        for exp in explist:
            try:
                self.currentType = None
                self.v_Node(exp)
            except SymanticError as SE:
                self.errors.append(SE)
            

    def v_Assignemnt(self,node):
        self.v_Node(node.lvalue)
        self.v_Node(node.rvalue)
    
    def v_ArrayRef(self,node):
        oldtype = self.currentType
        self.currentType = None
        self.v_Node(node.name)
        arraytype = self.getbase(self.currentType)
        self.currentType = None
        self.v_Node(node.subscript)
        if not self.checkIsInt(self.currentType):
            self.errors.append(SymanticError("Array subscript not an interger",node.cords))
        if arraytype.qual not in ["arr","ptr"]:
            raise SymanticError("Subscripting a non array",node.cords)
        self.currentType = oldtype
        self.checktype(arraytype.rtype,node)
    
    def v_Alignas(self,node):
        raise NotImplementedError
    
    def v_BinOp(self,node):
        self.v_Node(node.left)
        self.v_Node(node.right)
    
    def v_Break(self,node):
        raise NotImplementedError
    
    def v_Case(self,node):
        raise NotImplementedError
    
    def v_Cast(self,node):
        self.currentType = None
        self.v_Node(node.expr)
        self.currentType = node.to_type
    
    def v_Constant(self,node):
        self.checkconst(node.type,node)
    
    def v_Body(self,node):
        self.v_ExprList(node.exprs)
    
    def v_Continue(self,node):
        raise NotImplementedError
    
    def v_Decl(self,node):
        self.SymbolStack[-1].update({node.name:node.type})
        if node.init is not None:
            self.currentType = node.type
            self.v_Node(node.init)
    
    def v_Default(self,node):
        raise NotImplementedError
    
    def v_DoWhile(self,node):
        raise NotImplementedError
    
    def v_EllipsParm(self,node):
        pass

    def v_For(self,node):
        if node.init is not None:
            self.currentType = None
            self.v_Node(node.init)
        if node.cond is not None:
            self.currentType = None
            self.v_Node(node.cond)
        if node.next is not None:
            self.currentType = None
            self.v_Node(node.next)
        self.fordepth += 1
        self.v_ExprList(node.body)
        self.fordepth -= 1
    
    def v_FuncCall(self,node):
        functionprops = None
        if node.name.nodeName == "ID":
            functionprops = self.getSymbol(node.name.name,node.name)
        if functionprops.qual != "function":
            raise SymanticError(node.name +" is not a function",node.cords)
        temptype = self.currentType
        if functionprops.params is None:
            if(node.args is not None) and len(node.args) > 0:
                raise SymanticError("To much much args given")
        elif node.args is None:
            if(functionprops.params is not None) and len(functionprops.params) > 0:
                raise SymanticError("To litte props given")
        else:
            if len(node.args) > len(functionprops.params):
                raise SymanticError("To much args given",node.cords)
            if len(node.args) < len(functionprops.params):
                raise SymanticError("To little args",node.cords)
            for arg,parm in zip(node.args,functionprops.params):
                self.currentType = parm
                self.v_Node(arg)
        self.currentType = temptype
        self.checktype(functionprops.rtype,node)
    
    def v_FuncDef(self,node):
        self.addSymbol(node.name,node.type,node)
        self.SymbolStack.append({})
        for d in node.args:
            if d.init != None:
                raise SymanticError("No defult values in type decle",d.cords)
            self.addSymbol(d.name,d.type,d)
        self.returnType = node.type.rtype
        self.v_ExprList(node.body)
        self.SymbolStack.pop()
        
    
    def v_Goto(self,node):
        raise NotImplementedError
    
    def v_ID(self,node):
        propertys = self.getSymbol(node.name,node)
        self.checktype(propertys,node)
    
    def v_InitList(self,node):
        raise NotImplementedError
    
    def v_NamedInit(self,node):
        raise NotImplementedError
    
    def v_IfNode(self,node):
        self.v_Node(node.cond)
        if(node.iffalse != None):
            self.v_ExprList(node.iftrue)
        if(node.iffalse != None):
            self.v_ExprList(node.iffalse)
    
    def v_Label(self,node):
        raise NotImplementedError
    
    def v_Return(self,node):
       if str(self.checktype) == "void" and  node.expr != None:
            raise SymanticError("Attempted to return value on node function",node.cords)
       else:
           self.currentType = self.returnType
           self.v_Node(node.expr)
           
    
    def v_StructRef(self,node):
        oldtype = self.currentType
        self.currentType = None
        self.v_Node(node.name)
        structprops = self.getbase(self.currentType)
        if(node.type == "->"):
            if structprops.qual != "ptr":
                raise SymanticError("Attempting to deref a non pointer",node.cords)
            structprops = structprops.rtype
        structprops = self.getbase(structprops)
        if structprops.qual not in ["union","struct"]:
            raise SymanticError("Not a struct or union",node.cords)
        field = node.field.name
        if field not in structprops.members:
            raise SymanticError("struct has no member "+field,node.cords)
        self.currentType = oldtype
        self.checktype(structprops.members[field],node)
    
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
        return self.lookup[node.nodeName](node)
    

