_OFFSETSTR = "  "
_WRITELINE = lambda o,m: (o * _OFFSETSTR) + m
_PRINTLINE = lambda o,m:print(_WRITELINE(o,m))
_PRINTREC = lambda o:_PRINTLINE(o,"Recursion Deceted")

class jtype:

    def __init__(self,name,size = 4):
        self.name = name
        self.size = size
        self.qual = "base"
    
    def show(self,offset,shownStack = []):
        _PRINTLINE(offset,str(self))

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self))

    def __str__(self): return str(self.name)

    def __eq__(self,other):
        if other.qual != "base":
            return False
        return other.name == self.name

class jstype:

    def __init__(self,name,rtype):
        self.name = name
        self.rtype = rtype
        self.qual = "syth"
        self.size = self.rtype.size
    
    def __str__(self): return str(self.name)

    def __eq__(self,other):
        if other.qual != self.qual:
            return False
        else:
            return other.rtype == self.rtype

    def show(self,offset,shownStack = []):
        _PRINTLINE(offset,str(self) + ":")
        if(self.name in shownStack):
            _PRINTLINE(offset,"RECURSION DETECTED")
            return
        shownStack.append(self.name)
        self.rtype.show(offset + 1)
        shownStack.pop()

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self) + ":" + str(self.rtype))

class pointerType:

    def __init__(self,rtype):
        self.rtype = rtype
        self.qual = "ptr"
        self.size = 4
    
    def show(self,offset,shownStack = []):
        _PRINTLINE(offset,"ptr:")
        self.rtype.show(offset + 1,shownStack)

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self))

    def __str__(self): return str(self.rtype) + "*"

    def __eq__(self,other):
        if other.qual != "ptr":
            return False
        return other.rtype == self.rtype

class arrayType:

    def __init__(self,rtype,length):
        self.rtype = rtype
        self.length = length
        self.qual = "arr"
        self.size = 0
        self.isvarible = True
        if length != None:
            self.size = self.length.value * rtype.size
            self.isvarible = False

    def show(self,offset,shownStack = []):
        _PRINTLINE(offset,"array:")
        self.rtype.show(offset + 1,shownStack)

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self))

    def __str__(self):
        if self.isvarible: 
            return str(self.rtype) + "[]"
        else:
            return str(self.rtype) + "[" + str(self.length) + "]"
    
    def __eq__(self,other):
        if other.rtype != "arr":
            return False
        return self.rtype == other.rtype

class structType:

    def __init__(self,name,members,size = 4):
        self.name = name
        self.size = 0
        self.members = members
        self.qual = "struct"
        for mem in self.members:
            self.size += mem.size

    def show(self,offset,shownStack = []):
        if(self.name in shownStack):
            _PRINTLINE(offset,str(self))
            return
        _PRINTLINE(offset,str(self) + ":")
        if self.name in shownStack:
            _PRINTREC(offset)
            return
        shownStack.append(self.name)
        for mems in self.members.keys():
            _PRINTLINE(offset + 1,mems + ":")
            self.members[mems].show(offset + 2)
        shownStack.pop()

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self))
        for mems in self.members:
            _PRINTLINE(offset + 1,mems + ":" + str(self.members[mems]))

    def __str__(self):return str(self.name)

    def __eq__(self,other):
        return (other.qual == "struct") and (other.name == self.name)

class unionType:

    def __init__(self,name,members,size = 4):
        self.name = name
        self.size = 0
        self.members = members
        self.qual = "union"
        for mem in self.members:
            self.size = max(self.size,mem.size)

    def show(self,offset,shownStack = []):
        _PRINTLINE(offset,str(self) + ":")
        if self.name in shownStack:
            _PRINTREC(offset)
            return
        shownStack.append(self.name)
        for mems in self.members.keys():
            _PRINTLINE(offset + 1,mems + ":")
            self.members[mems].show(offset + 2)
        shownStack.pop()

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self))
        for mems in self.members:
            _PRINTLINE(offset + 1,mems + ":" + str(self.members[mems]))
    
    def __str__(self):
        return str(self.name)
    
    def __eq__(self,other):
        return (other.qual == "union") and (other.name == self.name)

class functionType:

    def __init__(self,params,rtype):
        self.rtype = rtype
        self.params = params
        self.qual = "function"
    
    def __str__(self):
        return str(self.rtype) + " function(" + ",".join([str(p) for p in self.params]) + ")"

class enumType:

    def __init__(self,name,members):
        self.name = name
        self.members = members
        self.qual = "enum"
        self.size = 1

    def __str__(self):
        mems = ",".join([str(m) for m in self.members.keys()])
        return str(self.name + " " + mems)

    def showBasic(self,offset):
        _PRINTLINE(offset,str(self))

    def show(self,offset):
        _PRINTLINE(offset,str(self.name))
        for mem in self.members.keys():
            _PRINTLINE(offset + 1,str(mem) + ":" + str(self.members[mem]))

    def __eq__(self,other):
        return (other.qual == "enum") and (other.name == self.name)

class typeTable:

    def __init__(self):
        self.table = self.genTable()

    def genTable(self):
        typeList = [
            ["unsigned char",1,"int"],
            ["unsigned short",2,"int"],
            ["unsigned int",4,"int"],
            ["unsigned long",8,"int"],
            ["unsigned long long",8,"int"],
            ["char",1,"int"],
            ["short",2,"int"],
            ["int",4,"int"],
            ["long",8,"int"],
            ["long long",8,"int"],
            ["float",4,"int"],
            ["double",8,"int"],
            ["_bool",1,""],
            ["void",0,""]
        ]
        table = {}
        for t in typeList:
            table.update({t[0]:jtype(t[0],t[1])})
        return table
    
    def updateTable(self,newType):
        self.table.update({newType.name:newType})

    def getRootType(self,Type,byname = True):
        if byname:
            Type = self.table[Type]
        if (Type.qual == "syth") or (Type.qual == "function"):
            return self.getRootType(Type.rtype)
        else:
            return Type

    def getType(self,typename):
        return self.table[typename]

    def hasType(self,typename):
        return typename in self.table.keys()

    def show(self,offset = 0):
        for mems in list(self.table.keys())[14:]:
            self.table[mems].show(offset)

    def showBasic(self,offset = 0):
        for mems in list(self.table.keys())[14:]:
            self.table[mems].showBasic(offset)