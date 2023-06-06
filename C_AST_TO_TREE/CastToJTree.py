from C_AST_TO_TREE.Jtype import *
import C_AST_TO_TREE.JTree as JTree

class compError(Exception):

    def __init__(self,message,loc):
        self.message = message
        self.loc = loc

    def __str__(self):
        return "Error at " + str(self.loc) + " " + str(self.message)

class CastToJTree:

    def __init__(self):
        self.nodename = lambda n:n.__class__.__name__
        self.funclist = self.initCodeLookup()
        self.rows = []
        self.typeTable = typeTable()
        self.inBlock = False

    def run(self,AST,rows = None):
        if rows != None:
            self.rows = rows
        return self.v_node(AST)
        

    def v_node(self,node):
        if node == None: return None
        return self.funclist[self.nodename(node)](node)

    def v_type(self,node):
        return self.v_node(node)

    
    def v_ArrayDecl(self,node):
        dim = node.dim
        if(dim != None):
            if self.nodename(dim) != "Constant":
                raise NotImplementedError
            if dim.type != "int":
                raise NotImplementedError
            dim = dim.value
        return arrayType(self.v_type(node.type),node.dim)

    def v_ArrayRef(self,node):
        return JTree.ArrayRef(self.v_node(node.name),self.v_node(node.subscript),node.coord)

    def v_Assignment(self,node):
        return JTree.Assignment(node.op,self.v_node(node.lvalue),self.v_node(node.rvalue))

    def v_Alignas(self,node):
        raise NotImplementedError

    def v_BinaryOp(self,node):
        return JTree.BinOp(self.v_node(node.left),node.op,self.v_node(node.right))

    def v_Break(self,node):
        return JTree.Break()

    def v_Case(self,node):
        return JTree.Case(self.v_node(node.expr),[self.v_node(n) for n in node.stmts],node.coord)

    def v_Cast(self,node):
        return JTree.Cast(self.v_type(node.to_type),self.v_node(node.expr),node.coord)

    def v_Compound(self,node):
        if node.block_items == None:
            return []
        return [self.v_node(n) for n in node.block_items]

    def v_CompoundLiteral(self,node):
        raise NotImplementedError

    def v_Constant(self,node):
        return JTree.Constant(str(node.type),node.value,node.coord)

    def v_Continue(self,node):
        return JTree.Continue(node.coord)

    def v_Decl(self,node):
        scope = "Block" if self.inBlock else "Global"
        storage = " ".join(node.storage)
        quals = " ".join(node.quals)
        if node.name != None:
            return JTree.Decl(node.name,self.v_type(node.type),scope,quals,storage,self.v_node(node.init),node.coord)
        else:
            self.v_node(node.type)




    def v_DeclList(self,node):
        if len(node.decls) == 1:
            return(self.v_node(node.decls[0]))
        return [self.v_node(n) for n in node.decls]

    def v_Default(self,node):
        return JTree.Default([self.v_node(n) for n in node.stmts],node.coord)

    def v_DoWhile(self,node):
        return JTree.DoWhile(self.v_node(node.cond),self.v_node(node.stmt),node.coord)

    def v_EllipsisParam(self,node):
        return JTree.EllipsParm(node.coord)

    def v_EmptyStatement(self,node):
        return None

    def v_Enum(self,node):
        enumName = "enum "+str(node.name)
        if node.name == None:
            enumName = "enum"
        if self.typeTable.hasType(enumName):
            return self.typeTable.getType(enumName)
        members = self.v_EnumeratorList(node.values)
        enum = enumType(enumName,members)
        if node.name != None:
            self.typeTable.updateTable(enum)
        return enum

    def v_Enumerator(self,node):
        name = node.name
        if node.value != None:
            if self.nodename(node.value) == "Constant":
                if node.value.type == "int":
                    return {name:node.value.value}
                else:
                    raise compError("Enum values cannot be non int const",node.coord)
            else:
                raise compError("Enum value must be a constant",node.coord)
        return {name:None}

    def v_EnumeratorList(self,node):
        members = {}
        if node == None:
            return members
        for en in node.enumerators:
            members.update(self.v_Enumerator(en))
        return members

    def v_ExprList(self,node):
        if node == None:
            return []
        return [self.v_node(n) for n in node.exprs]

    def v_FileAST(self,node):
        nodes = []
        for n in node.ext:
            proccessed = self.v_node(n)
            if proccessed != None:
                nodes.append(proccessed)
        return JTree.Body(nodes,node.coord)

    def v_For(self,node):
        init = self.v_node(node.init)
        return JTree.For(init,
        self.v_node(node.cond),
        self.v_node(node.stmt),
        self.v_node(node.next))

    def v_FuncCall(self,node):
        return JTree.FuncCall(self.v_node(node.name),self.v_node(node.args))

    def v_FuncDecl(self,node):
        args = []
        if node.args != None:
            args = self.v_ParamDecls(node.args)
        rtype = self.v_type(node.type)
        return functionType(args,rtype)

    def v_FuncDef(self,node):
        FuncDec = node.decl.type
        args = []
        self.inBlock = True
        args = self.v_ParamList(node.decl.type.args)
        FuncType = self.v_FuncDecl(node.decl.type)
        Body = self.v_node(node.body)
        self.inBlock = False
        return JTree.FuncDef(node.decl.name,FuncType,args,Body,node.coord)

    def v_Goto(self,node):
        return JTree.Goto(node.name,node.coord)

    def v_ID(self,node):
        return JTree.ID(node.name,node.coord)

    def v_IdentifierType(self,node):
        typeName = " ".join(node.names)
        return self.typeTable.getType(typeName)

    def v_If(self,node):
        return JTree.IfNode(self.v_node(node.cond),
        self.v_node(node.iftrue),
        self.v_node(node.iffalse),node.coord)

    def v_InitList(self,node):
        return JTree.InitList([self.v_node(n) for n in node.exprs])

    def v_Label(self,node):
        return JTree.Label(node.name,self.v_node(node.stmt),node.coord)

    def v_NamedInitializer(self,node):
        return JTree.NamedInit([self.v_node(n) for n in node.name],self.v_node(node.expr))

    def v_ParamList(self,node):
        if (node == None) or (node.params == None):
            return []
        return [self.v_node(n) for n in node.params]

    def v_ParamDecls(self,node):
        if (node == None) or (node.params == None):
            return
        Decls = []
        for n in node.params:
            if self.nodename(n) == "EllipsisParam":
                Decls.append(JTree.EllipsParm())
            elif self.nodename(n) == "ID":
                raise NotImplementedError
            else:
                Decls.append(self.v_type(n.type))
        return Decls

    def v_PtrDecl(self,node):
        return pointerType(self.v_node(node.type))

    def v_Return(self,node):
        return JTree.Return(self.v_node(node.expr),node.coord)

    def v_StaticAssert(self,node):
        raise NotImplementedError

    def v_Struct(self,node):
        if node.decls == None:
            if self.typeTable.hasType("struct "+str(node.name)):
                return self.typeTable.getType("struct "+str(node.name))
            return None
        nodeName = "struct"
        if node.name != None:
            nodeName += " " + str(node.name)
        newstruct = structType(nodeName,{})
        if node.name != None:
            self.typeTable.updateTable(newstruct)
        for decs in node.decls:
            if self.nodename(decs) != "Decl":
                raise NotImplementedError
            nameANDtype = self.v_Decl(decs)
            if (nameANDtype.name == None) or (nameANDtype.init != None):
                raise NotImplementedError
            newstruct.members.update({nameANDtype.name:nameANDtype.type})
        return newstruct

    def v_StructRef(self,node):
        return JTree.StructRef(self.v_node(node.name),node.type,self.v_node(node.field),node.coord)

    def v_Switch(self,node):
        return JTree.Switch(self.v_node(node.cond),self.v_node(node.stmt),node.coord)

    def v_TernaryOp(self,node):
        return JTree.TernaryOp(self.v_node(node.cond),self.v_node(node.iftrue),self.v_node(node.iffalse))

    def v_TypeDecl(self,node):
        return self.v_node(node.type)

    def v_Typedef(self,node):
        rtype = self.v_type(node.type)
        name = node.name
        self.typeTable.updateTable(jstype(name,rtype))

    def v_Typename(self,node):
        return self.v_type(node.type)

    def v_UnaryOp(self,node):
        return JTree.UnaryOp(node.op,self.v_node(node.expr),node.coord)

    def v_Union(self,node):
        if node.decls == None:
            if self.typeTable.hasType("union "+str(node.name)):
                return self.typeTable.getType("union "+str(node.name))
            return None
        nodeName = "union"
        if node.name != None:
            nodeName += " " + str(node.name)
        newunion = unionType(nodeName,{})
        for decs in node.decls:
            if self.nodename(decs) != "Decl":
                raise NotImplementedError
            nameANDtype = self.v_Decl(decs)
            if (nameANDtype.name == None) or (nameANDtype.init != None):
                raise NotImplementedError
            newunion.members.update({nameANDtype.name:nameANDtype.type})
        if node.name != None:
            self.typeTable.updateTable(newunion)
        return newunion

    def v_While(self,node):
        return JTree.While(self.v_node(node.cond),self.v_node(node.stmt),node.coord)

    def v_Pragma(self,node):
        raise NotImplementedError

    def initCodeLookup(self):
        return {"ArrayDecl":self.v_ArrayDecl,
            "ArrayRef":self.v_ArrayRef,
            "Assignment":self.v_Assignment,
            "Alignas":self.v_Alignas,
            "BinaryOp":self.v_BinaryOp,
            "Break":self.v_Break,
            "Case":self.v_Case,
            "Cast":self.v_Cast,
            "Compound":self.v_Compound,
            "CompoundLiteral":self.v_CompoundLiteral,
            "Continue":self.v_Continue,
            "Constant":self.v_Constant,
            "Decl":self.v_Decl,
            "DeclList":self.v_DeclList,
            "Default":self.v_Default,
            "DoWhile":self.v_DoWhile,
            "EllipsisParam":self.v_EllipsisParam,
            "EmptyStatement":self.v_EmptyStatement,
            "Enum":self.v_Enum,
            "Enumerator":self.v_Enumerator,
            "EnumeratorList":self.v_EnumeratorList,
            "ExprList":self.v_ExprList,
            "FileAST":self.v_FileAST,
            "For":self.v_For,
            "FuncCall":self.v_FuncCall,
            "FuncDecl":self.v_FuncDecl,
            "FuncDef":self.v_FuncDef,
            "Goto":self.v_Goto,
            "ID":self.v_ID,
            "IdentifierType":self.v_IdentifierType,
            "If":self.v_If,
            "InitList":self.v_InitList,
            "Label":self.v_Label,
            "NamedInitializer":self.v_NamedInitializer,
            "ParamList":self.v_ParamList,
            "PtrDecl":self.v_PtrDecl,
            "Return":self.v_Return,
            "StaticAssert":self.v_StaticAssert,
            "Struct":self.v_Struct,
            "StructRef":self.v_StructRef,
            "Switch":self.v_Switch,
            "TernaryOp":self.v_TernaryOp,
            "TypeDecl":self.v_TypeDecl,
            "Typedef":self.v_Typedef,
            "Typename":self.v_Typename,
            "UnaryOp":self.v_UnaryOp,
            "Union":self.v_Union,
            "While":self.v_While,
            "Pragma":self.v_Pragma}