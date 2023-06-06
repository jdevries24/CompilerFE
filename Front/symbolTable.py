class symbol:

    def __init__(self,type,name,scope):
        self.name = name
        self.type = type
        self.scope = scope
    
    def __str__(self):
        return str(self.type) + " " + str(self.name) + " " + str(self.scope)

class symbolTable:

    def __init__(self):
        self.scopeStack = [[]]

    def addSymbol(self,symbol):
        self.scopeStack[-1].append(symbol)

    def searchSymbols(self,name):
        for lists in self.scopeStack[::-1]:
            for sym in lists:
                if sym.name == name:
                    return name
        return None

    def pushScope(self):
        self.scopeStack.append([])

    def popScope(self):
        self.scopeStack.pop()
    
    def __str__(self):
        symFlattened = []
        for substacks in self.scopeStack:
            for sym in substacks:
                symFlattened.append(sym)
        return "\n".join([str(s) for s in symFlattened])
