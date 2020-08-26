import copy
varDict = {}
functDict = {}
class Node():
    def __init__(self):
        self.parent = None
    def typecheck(self):
        return True
    def parentCount(self):
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count
class Variable(Node):
    def __init__(self, name, var = varDict):
        super().__init__()
        self.var = var
        self.name = name
    def eval(self):
        if isinstance(self.var, Variable):
            if isinstance(self.var.name, int) or isinstance(self.var.name, str):
                if self.var.name is None:
                    return None
            else:
                if self.var.name.eval() is None:
                    return None
            if self.var.eval() is None:
                return None
        else:
            if self.var is None:
                return None
        if isinstance(self.name, str) or isinstance(self.name, int):
            if self.name is None: 
                return None
        else:
            if self.name.eval() is None:
                return None
        if isinstance(self.name, str) or isinstance(self.name, int):
            if isinstance(self.var, Variable):
                if isinstance(self.var.name, int) or isinstance(self.var.name, str):
                    return self.var.getVar()[self.var.name][self.name]
                else:
                    return self.var.getVar()[self.var.name.eval()][self.name]
            return self.var[self.name]
        else:
            if isinstance(self.var, Variable):
                if isinstance(self.var.name, int) or isinstance(self.var.name, str):
                    return self.var.getVar()[self.var.name][self.name.eval()]
                else:
                    return self.var.getVar()[self.var.name.eval()][self.name.eval()]
            return self.var[self.name.eval()]
    def getVar(self):
        if self.var is None:
            return {}
        if isinstance(self.var, Variable):
            return self.var.eval() #You should only call this if the var is a Variable Object
        else:
            return self.var
    def typecheck(self):
        if isinstance(self.var, Variable):
            if not self.var.typecheck():
                return False
            if isinstance(self.name, Node):
                if self.name.typecheck():
                    if isinstance(self.name.eval(), int):
                        if(self.name.eval() < len(self.var.getVar()) and self.name.eval() >= 0):
                            return True
                    print("SEMANTIC ERROR")
                    return False
        elif isinstance(self.name, Node):
            if self.name.typecheck():
                if isinstance(self.name.eval(), int):
                    if(self.name.eval() < len(self.var) and self.name.eval() >= 0):
                        return True
                print("SEMANTIC ERROR")
                return False
        elif self.name in self.var:
            return True
        print("SEMANTIC ERROR")
        return False
class Code():
    def __init__(self):
        self.parent = None
    def typecheck(self):
        return True
class Print(Code):
    def __init__(self, node):
        self.node = node
    def eval(self):
        print(self.node.eval())
    def typecheck(self):
        return self.node.typecheck()
class Block(Code):
    def __init__(self, statements = []): #Statement is a list of code
        self.statements = statements
    def add_smt(self, statement):
        self.statements += statement
    def eval(self):
        for smt in self.statements:
            smt.eval()
    def typecheck(self):
        for smt in self.statements:
            if not smt.typecheck():
                return False
        return True
class Set(Code):
    def __init__(self, node, var):
        super().__init__()
        self.node = node
        self.var = var
        if(self.node.typecheck() and isinstance(self.var.name, str)):
            self.var.getVar()[self.var.name] = self.node.eval()
        elif isinstance(self.var.name, Node) or isinstance(self.var.name, int):
            pass
        else:
            raise ValueError()
    def eval(self):
        if isinstance(self.var.name, Node):
            self.var.getVar()[self.var.name.eval()] = self.node.eval()
        else:
            self.var.getVar()[self.var.name] = self.node.eval()

    def typecheck(self):
        return self.node.typecheck() and self.var.typecheck()
class If(Code):
    def __init__(self, node, block):
        super().__init__()
        self.node = node
        self.block = block
    def eval(self):
        if self.node.eval():
            self.block.eval()
    def typecheck(self):
        if self.node.typecheck():
            if isinstance(self.node.eval(), bool):
                return self.block.typecheck()
            else:
                print("SEMANTIC ERROR")
        return False
class IfElse(Code):
    def __init__(self, node, block1, block2):
        super().__init__()
        self.node = node
        self.block1 = block1
        self.block2 = block2
    def eval(self):
        # print("Evaluating an IFELSE")
        if self.node.eval():
            self.block1.eval()
        else: 
            self.block2.eval()
    def typecheck(self):
        if self.node.typecheck():
            if isinstance(self.node.eval(), bool):
                if self.block1.typecheck():
                    return self.block2.typecheck()
            else:
                print("SEMANTIC ERROR")
        return False
class While(Code):
    def __init__(self, node, block):
        super().__init__()
        self.node = node
        self.block = block
    def eval(self):
        while(self.node.eval()):
            self.block.eval()
    def typecheck(self):
        if self.node.typecheck():
            if isinstance(self.node.eval(), bool):
                return self.block.typecheck()
            else:
                print("SEMANTIC ERROR")
        return False

class Funct(Code):
    def __init__(self, name, args, block, expr):
        self.name = name
        self.args = args 
        self.block = block
        self.expr  = expr
        functDict[name] = self
        for arg in self.args:
            if not isinstance(arg, str):
                print("SEMANTIC ERROR")
                raise ValueError()
        if not self.block.typecheck():
            raise ValueError()
    def getArgs(self):
        return self.args
    def eval(self):
        self.block.eval()
        return self.expr.eval()
    def typecheck(self):
        return True
class FunctExec(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args #args is the Args Object 
    def eval(self):
        if functDict[self.name] is None:
            return 0
        argsCopy = {}
        argsStack = []
        args = self.args.eval()
        functArgs = functDict[self.name].getArgs()
        for arg in functArgs:
            if arg in varDict:
                argsCopy[arg] = copy.deepcopy(varDict[arg])
            else:
                argsStack.append(arg)

        for i in range(len(functArgs)):
            if isinstance(args[i], Node):
                varDict[functArgs[i]] = args[i].eval()
            else:
                varDict[functArgs[i]] = args[i]
            
        returnVal = functDict[self.name].eval()
        for arg in argsCopy:
            varDict[arg] = argsCopy[arg]
        for arg in argsStack:
            varDict.pop(arg, None)
        return returnVal
    def typecheck(self):
        if not self.name in functDict:
            print("SEMANTIC ERROR")
            return False
        if not self.args.typecheck():
            return False
        if not functDict[self.name] is None:
            if len(self.args.eval()) != len(functDict[self.name].getArgs()):
                print("SEMANTIC ERROR")
                return False
            return functDict[self.name].typecheck()
        return True