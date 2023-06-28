_PRINTLINE = lambda o,l: print(("  " * o) + str(l))
class JNode:
    pass



class Assignment:

    def __init__(self,op = None,lvalue = None,rvalue = None,cords = None):
        self.nodeName = "Assignment"
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.cords = cords

    def __iter__(self):
        yield self.op
        yield self.lvalue
        yield self.rvalue

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.op))
        _PRINTLINE(offset + 1,"lvalue:")
        if self.lvalue is not None:
            self.lvalue.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"rvalue:")
        if self.rvalue is not None:
            self.rvalue.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class ArrayRef:

    def __init__(self,name = None,subscript = None,cords = None):
        self.nodeName = "ArrayRef"
        self.name = name
        self.subscript = subscript
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.subscript

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"name:")
        if self.name is not None:
            self.name.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"subscript:")
        if self.subscript is not None:
            self.subscript.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Alignas:

    def __init__(self,alingment = None,cords = None):
        self.nodeName = "Alignas"
        self.alingment = alingment
        self.cords = cords

    def __iter__(self):
        yield self.alingment

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.alingment))

    def __str__(self):
        return str(self.nodeName)

class BinOp:

    def __init__(self,left = None,op = None,right = None,cords = None):
        self.nodeName = "BinOp"
        self.left = left
        self.op = op
        self.right = right
        self.cords = cords

    def __iter__(self):
        yield self.left
        yield self.op
        yield self.right

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.op))
        _PRINTLINE(offset + 1,"left:")
        if self.left is not None:
            self.left.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"right:")
        if self.right is not None:
            self.right.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Break:

    def __init__(self):
        self.nodeName = "Break"

    def __iter__(self):
        return
        yield

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")

    def __str__(self):
        return str(self.nodeName)

class Case:

    def __init__(self,expr = None,stmts = None,cords = None):
        self.nodeName = "Case"
        self.expr = expr
        self.stmts = stmts
        self.cords = cords

    def __iter__(self):
        yield self.expr
        yield self.stmts

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"expr:")
        if self.expr is not None:
            self.expr.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"stmts:")
        if self.stmts is not None:
            for node in self.stmts:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Cast:

    def __init__(self,to_type = None,expr = None,cords = None):
        self.nodeName = "Cast"
        self.to_type = to_type
        self.expr = expr
        self.cords = cords

    def __iter__(self):
        yield self.to_type
        yield self.expr

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"to_type:")
        if self.to_type is not None:
            self.to_type.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"expr:")
        if self.expr is not None:
            self.expr.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Constant:

    def __init__(self,type = None,value = None,cords = None):
        self.nodeName = "Constant"
        self.type = type
        self.value = value
        self.cords = cords

    def __iter__(self):
        yield self.type
        yield self.value

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.type)+ ", " +str(self.value))

    def __str__(self):
        return str(self.nodeName)

class Body:

    def __init__(self,exprs = None,cords = None):
        self.nodeName = "Body"
        self.exprs = exprs
        self.cords = cords

    def __iter__(self):
        yield self.exprs

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"exprs:")
        if self.exprs is not None:
            for node in self.exprs:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Continue:

    def __init__(self):
        self.nodeName = "Continue"

    def __iter__(self):
        return
        yield

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")

    def __str__(self):
        return str(self.nodeName)

class Decl:

    def __init__(self,name = None,type = None,scope = None,qual = None,storage = None,init = None,cords = None):
        self.nodeName = "Decl"
        self.name = name
        self.type = type
        self.scope = scope
        self.qual = qual
        self.storage = storage
        self.init = init
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.type
        yield self.scope
        yield self.qual
        yield self.storage
        yield self.init

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.name)+ ", " +str(self.type)+ ", " +str(self.scope)+ ", " +str(self.qual)+ ", " +str(self.storage))
        _PRINTLINE(offset + 1,"init:")
        if self.init is not None:
            self.init.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Default:

    def __init__(self,stmts = None,cords = None):
        self.nodeName = "Default"
        self.stmts = stmts
        self.cords = cords

    def __iter__(self):
        yield self.stmts

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"stmts:")
        if self.stmts is not None:
            for node in self.stmts:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class DoWhile:

    def __init__(self,cond = None,stmts = None,cords = None):
        self.nodeName = "DoWhile"
        self.cond = cond
        self.stmts = stmts
        self.cords = cords

    def __iter__(self):
        yield self.cond
        yield self.stmts

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"cond:")
        if self.cond is not None:
            self.cond.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"stmts:")
        if self.stmts is not None:
            for node in self.stmts:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class EllipsParm:

    def __init__(self):
        self.nodeName = "EllipsParm"

    def __iter__(self):
        return
        yield

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")

    def __str__(self):
        return str(self.nodeName)

class For:

    def __init__(self,init = None,cond = None,body = None,next = None,cords = None):
        self.nodeName = "For"
        self.init = init
        self.cond = cond
        self.body = body
        self.next = next
        self.cords = cords

    def __iter__(self):
        yield self.init
        yield self.cond
        yield self.body
        yield self.next

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"init:")
        if self.init is not None:
            self.init.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"cond:")
        if self.cond is not None:
            self.cond.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"body:")
        if self.body is not None:
            for node in self.body:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"next:")
        if self.next is not None:
            self.next.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class FuncCall:

    def __init__(self,name = None,args = None,cords = None):
        self.nodeName = "FuncCall"
        self.name = name
        self.args = args
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.args

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.name))
        _PRINTLINE(offset + 1,"args:")
        if self.args is not None:
            for node in self.args:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class FuncDef:

    def __init__(self,name = None,type = None,args = None,body = None,cords = None):
        self.nodeName = "FuncDef"
        self.name = name
        self.type = type
        self.args = args
        self.body = body
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.type
        yield self.args
        yield self.body

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.name)+ ", " +str(self.type))
        _PRINTLINE(offset + 1,"args:")
        if self.args is not None:
            for node in self.args:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"body:")
        if self.body is not None:
            for node in self.body:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Goto:

    def __init__(self,name = None,cords = None):
        self.nodeName = "Goto"
        self.name = name
        self.cords = cords

    def __iter__(self):
        yield self.name

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.name))

    def __str__(self):
        return str(self.nodeName)

class ID:

    def __init__(self,name = None,cords = None):
        self.nodeName = "ID"
        self.name = name
        self.cords = cords

    def __iter__(self):
        yield self.name

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.name))

    def __str__(self):
        return str(self.nodeName)

class InitList:

    def __init__(self,inits = None,cords = None):
        self.nodeName = "InitList"
        self.inits = inits
        self.cords = cords

    def __iter__(self):
        yield self.inits

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"inits:")
        if self.inits is not None:
            for node in self.inits:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class NamedInit:

    def __init__(self,name = None,expr = None,cords = None):
        self.nodeName = "NamedInit"
        self.name = name
        self.expr = expr
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.expr

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"name:")
        if self.name is not None:
            for node in self.name:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"expr:")
        if self.expr is not None:
            self.expr.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class IfNode:

    def __init__(self,cond = None,iftrue = None,iffalse = None,cords = None):
        self.nodeName = "IfNode"
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.cords = cords

    def __iter__(self):
        yield self.cond
        yield self.iftrue
        yield self.iffalse

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"cond:")
        if self.cond is not None:
            self.cond.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"iftrue:")
        if self.iftrue is not None:
            for node in self.iftrue:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"iffalse:")
        if self.iffalse is not None:
            for node in self.iffalse:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Label:

    def __init__(self,name = None,stmts = None,cords = None):
        self.nodeName = "Label"
        self.name = name
        self.stmts = stmts
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.stmts

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.name))
        _PRINTLINE(offset + 1,"stmts:")
        if self.stmts is not None:
            for node in self.stmts:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class Return:

    def __init__(self,expr = None,cords = None):
        self.nodeName = "Return"
        self.expr = expr
        self.cords = cords

    def __iter__(self):
        yield self.expr

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"expr:")
        if self.expr is not None:
            self.expr.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class StructRef:

    def __init__(self,name = None,type = None,field = None,cords = None):
        self.nodeName = "StructRef"
        self.name = name
        self.type = type
        self.field = field
        self.cords = cords

    def __iter__(self):
        yield self.name
        yield self.type
        yield self.field

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.type))
        _PRINTLINE(offset + 1,"name:")
        if self.name is not None:
            self.name.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"field:")
        if self.field is not None:
            self.field.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class SizeOf:

    def __init__(self,type = None,cords = None):
        self.nodeName = "SizeOf"
        self.type = type
        self.cords = cords

    def __iter__(self):
        yield self.type

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.type))

    def __str__(self):
        return str(self.nodeName)

class Switch:

    def __init__(self,cond = None,stmts = None,cords = None):
        self.nodeName = "Switch"
        self.cond = cond
        self.stmts = stmts
        self.cords = cords

    def __iter__(self):
        yield self.cond
        yield self.stmts

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"cond:")
        if self.cond is not None:
            self.cond.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"stmts:")
        if self.stmts is not None:
            for node in self.stmts:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class TernaryOp:

    def __init__(self,cond = None,iftrue = None,iffalse = None,cords = None):
        self.nodeName = "TernaryOp"
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.cords = cords

    def __iter__(self):
        yield self.cond
        yield self.iftrue
        yield self.iffalse

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"cond:")
        if self.cond is not None:
            self.cond.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"iftrue:")
        if self.iftrue is not None:
            self.iftrue.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"iffalse:")
        if self.iffalse is not None:
            self.iffalse.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class UnaryOp:

    def __init__(self,op = None,expr = None,cords = None):
        self.nodeName = "UnaryOp"
        self.op = op
        self.expr = expr
        self.cords = cords

    def __iter__(self):
        yield self.op
        yield self.expr

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName) + ": " +str(self.op))
        _PRINTLINE(offset + 1,"expr:")
        if self.expr is not None:
            self.expr.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)

class While:

    def __init__(self,cond = None,stmt = None,cords = None):
        self.nodeName = "While"
        self.cond = cond
        self.stmt = stmt
        self.cords = cords

    def __iter__(self):
        yield self.cond
        yield self.stmt

    def show(self,offset = 0):
        _PRINTLINE(offset,str(self.nodeName)+":")
        _PRINTLINE(offset + 1,"cond:")
        if self.cond is not None:
            self.cond.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")
        _PRINTLINE(offset + 1,"stmt:")
        if self.stmt is not None:
            for node in self.stmt:
                if node != None:
                    node.show(offset + 2)
        else:
            _PRINTLINE(offset + 1,"None")

    def __str__(self):
        return str(self.nodeName)