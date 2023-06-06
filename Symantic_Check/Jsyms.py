
class jsym:

    def __init__(self,name,stype):
        self.name = name
        self.stype = stype
        
    
class symbolTable:

    def __init__(self):
        self.scopeStack = [[]]

    def addSymbol(self,symbol):
        self.scopeStack[-1].append(symbol)

    def searchSymbols(self,name):
        for lists in self.scopeStack[::-1]:
            for sym in lists:
                if sym.name == name:
                    return sym
        return None

    def pushScope(self):
        self.scopeStack.append([])

    def popScope(self):
        self.scopeStack.pop()