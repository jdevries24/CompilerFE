base = """

_OFFSETSTR = "  "
_WRITELINE = lambda o,m: (o * _OFFSETSTR) + m
_PRINTLINE = lambda o,m:print(_WRITELINE(o,m))
class JNode:

    def show(self,offset = 0):
        _PRINTLINE(offset,self.nodeName)
        for child in self.var():
            if child[1] == None:
                continue
            if type(child[1]) not in [str,int,list]:
                _PRINTLINE(offset + 1,child[0] + ":")
                child[1].show(offset + 2)
            elif type(child[1]) == list:
                _PRINTLINE(offset + 1,child[0] + ":")
                self.showList(child[1],offset + 1)
            else:
                _PRINTLINE(offset + 1,child[0] +": " + str(child[1]))

    def showList(self,list,offset):
        for thing in list:
            if thing == None:
                continue
            elif type(thing) in [str,int]:
                _PRINTLINE(offset + 1,str(thing))
            else:
                thing.show(offset + 1)


"""

def parseNode(nodeTxt):
    name = nodeTxt.split(' ')[0]
    children = nodeTxt.split(' ')[1]
    if children != "[]":
        children = children[1:-1].split(",")
    else:
        children = []
    return name,children

codeline = lambda offset,line : (offset * "    ") + line

def genClass(nodeTxt):
    name,children = parseNode(nodeTxt)
    overideShow = name[0] == "*"
    if overideShow:
        name = name[1:]
    children += ["cord"]
    base = "class " + name + "(JNode):\n"
    initFunc = codeline(1,"def __init__(self,") + ",".join([child + "=None" for child in children]) + "):\n"
    initFunc += "\n".join([codeline(2,"self." + child + " = " + child) for child in children])
    initFunc += '\n' + codeline(2,"self.nodeName =\"" + name) + '"\n\n'
    varfunc = codeline(1,"def var(self):\n")
    children.pop()
    if children == []:
        varfunc += codeline(2,"return\n") + codeline(2,"yield")
    varfunc += "\n".join([codeline(2,"if self." + child + " != None:\n") + codeline(3,"yield (\""+child+"\",self."+child + ")") for child in children]) + "\n\n"
    itterfunc = codeline(1,"def __iter__(self):\n")
    if children == []:
        itterfunc += codeline(2,"return\n") + codeline(2,"yield")
    itterfunc += "\n".join([codeline(2,"yield self." + child) for child in children])
    if overideShow:
        itterfunc += '\n\n' + codeline(1,'def show(self,offset):\n') + codeline(2,'_PRINTLINE(offset,self.nodeName + " " + ",".join([str(thing) for thing in self]))') + '\n\n'
    return base + initFunc + varfunc + itterfunc + '\n\n'

def genCode(nodeFtext):
    classes = []
    for nodeTxt in nodeFtext.split('\n'):
        if "//" in nodeTxt:
            continue
        classes.append(genClass(nodeTxt))
    return base + "\n\n".join(classes)

def cfgFile2pyFile(infile,ofile):
    with open(infile,'r') as IN:
        with open(ofile,'w') as OUT:
            OUT.write(genCode(IN.read()))

def writeVs(v_list):
    vL = []
    for v in v_list:
        vL.append(codeline(1,"def v_"+v+"(self,node):\n") + codeline(2,"raise NotImplementedError"))
    return "\n\n".join(vL)

def vlDic(v_list):
    vD = []
    for v in v_list:
        vD.append(codeline(3,'"' + v + '":self.v_' + v ))
    code = codeline(1,"def initCodeLookup(self):\n") + codeline(2,"return {")
    return code + ",\n".join(vD)[:-2] + "}"

def cfg_to_vlist(vinfo):
    vl = []
    for items in vinfo.split('\n'):
        vl.append(items.split(' ')[0])
    return vl

def cfgFile2VisitFile(infname,ofname):
    with open(infname,'r') as IN:
        with open(ofname,'w') as OUT:
            vlist = IN.read().split('\n')
            vlist = [line.split(' ')[0][:-1] for line in vlist]
            OUT.write(writeVs(vlist) + '\n\n' + vlDic(vlist))

if __name__ == "__main__":
    def main():
        cfgFile2VisitFile("C_AST_TO_TREE\\JNode2.cfg","Front\\SymanticCheck.py")
    main()
