

class JYACC:
    _WRITELINE = lambda o,l: ("    " * o) + str(l)

    def run(InputStr):
        base = [JYACC._WRITELINE(0,'_PRINTLINE = lambda o,l: print(("  " * o) + str(l))'),
        JYACC._WRITELINE(0,"class JNode:"),JYACC._WRITELINE(1,"pass"),"",""]
        nodes = ["\n".join(base)]
        for lines in InputStr.split('\n'):
            if(lines.strip() == "") or (lines.strip()[0] == "#"):
                continue
            nodes.append(JYACC.WriteNode(lines))
        return "\n\n".join(nodes)

    def WriteNode(nodeDef):
        name,args = JYACC.readNode(nodeDef)
        lines = [JYACC._WRITELINE(0,"class "+name+":")]
        lines.append(JYACC.writeInit(name,args))
        lines.append(JYACC.writeItter(name,args))
        lines.append(JYACC.writeShow(name,args))
        lines.append(JYACC._WRITELINE(1,"def __str__(self):") + '\n' + JYACC._WRITELINE(2,"return str(self.nodeName)"))
        return "\n\n".join(lines)

    def writeInit(name,args):
        params = ",".join([a[1] + " = None" for a in args])
        if args != []:
            params = "," + params
        lines = [JYACC._WRITELINE(1,"def __init__(self" + params + "):"),
        JYACC._WRITELINE(2,"self.nodeName = \"" + name + "\"")]
        lines += [JYACC._WRITELINE(2,"self." + a[1] + " = " + a[1]) for a in args]
        return "\n".join(lines)

    def writeItter(name,args):
        lines = [JYACC._WRITELINE(1,"def __iter__(self):")]
        if len(args) > 1:
            lines += [JYACC._WRITELINE(2,"yield self." + a[1]) for a in args[:-1]]
        else:
            lines += [JYACC._WRITELINE(2,"return"),
            JYACC._WRITELINE(2,"yield")]
        return "\n".join(lines)

    def writeShow(name,args):
        vals = []
        nodes = []
        for a in args[:-1]:
            if a[0] == 'v':
                vals.append(a[1])
            else:
                nodes.append(a)
        lines = [JYACC._WRITELINE(1,"def show(self,offset = 0):")]
        if vals != []:
            rootline = JYACC._WRITELINE(2,"_PRINTLINE(offset,str(self.nodeName) + \": \" +")
            rootline += '+ ", " +'.join(["str(self." + a +")" for a in vals])
            lines.append(rootline +")")
        else:
            lines.append(JYACC._WRITELINE(2,"_PRINTLINE(offset,str(self.nodeName)+\":\")"))
        for n in nodes:
            lines += [JYACC._WRITELINE(2,"_PRINTLINE(offset + 1,\"" + n[1] + ":\")"),JYACC._WRITELINE(2,"if self."+n[1] + " != None:")]
            if n[0] == "n":
                lines += [JYACC._WRITELINE(3,"self."+n[1] + ".show(offset + 2)")]
            else:
                lines += [JYACC._WRITELINE(3,"for node in self." + n[1] + ":"),
                JYACC._WRITELINE(4,"if node != None:"),
                JYACC._WRITELINE(5,"node.show(offset + 2)")]
            lines += [JYACC._WRITELINE(2,"else:"),JYACC._WRITELINE(3,"_PRINTLINE(offset + 1,\"None\")")]
        return "\n".join(lines)


    def readNode(nodeDef):
        parts = nodeDef.split(' ')
        name = parts[0][:-1]
        if parts[1] == "[]":
            return name,[]
        argDef = " ".join(parts[1:])[1:-1].split(", ")
        return name,JYACC.readArgs(argDef)

    def readArgs(argDef):
        args = []
        for arg in argDef:
            if len(arg) < 2:
                args.append(("v",arg))
            elif arg[-2:] == "**":
                args.append(("l",arg[:-2]))
            elif arg[-1:] == "*":
                args.append(("n",arg[:-1]))
            else:
                args.append(("v",arg))
        return args + [("n","cords")] 

with open("C_AST_TO_TREE\\JNode2.cfg") as F:
    with open("C_AST_TO_TREE\\JTree.py",'w') as O:
        O.write(JYACC.run(F.read()))

