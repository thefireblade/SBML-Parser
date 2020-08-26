#Jason Huang 110779373
import numbers
import copy
import ASTExtension as ASTNodes
# Type ASTNodes.Node
class Real(ASTNodes.Node):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def eval(self):
        return float(self.val)
class Int(ASTNodes.Node):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def eval(self):
        return int(self.val)

class Str(ASTNodes.Node):
    def __init__(self, val = "\'\'"):
        super().__init__()
        self.val = val[1:]
        self.val = self.val[:-1]
    def eval(self):
        return self.val
    def typecheck(self):
        if '\'' in self.val or '"' in self.val:
            print("SYNTAX ERROR")
            return False
        return True

class Bool(ASTNodes.Node):
    def __init__(self, val):
        super().__init__()
        self.val = val
    def eval(self):
        if self.val == 'True':
            return True
        else:
            return False


class Args(ASTNodes.Node):
    def __init__(self):
        super().__init__()
        self.args = []
    def add_arg(self, node):
        self.args.append(node)
    def get_args(self):
        return self.args
    def merge_args(self, args):
        self.args += args
    def eval(self):
        return [arg.eval() for arg in self.args]
    def typecheck(self):
        for arg in self.args:
            if not arg.typecheck():
                return False
        return True

class Tuple(ASTNodes.Node):
    def __init__(self, args=Args(), mode=0):
        super().__init__()
        self.args = args
        self.tuple = ()
        self.mode = mode
    def eval(self):
        if self.mode == 0:
            return tuple(arg for arg in self.args.eval())
        else:
            return self.tuple
    def typecheck(self):
        if self.mode == 0:
            return self.args.typecheck()
        else:
            return True

class List(ASTNodes.Node):
    def __init__(self, args=Args(), mode=0):
        super().__init__()
        self.args = args
        self.args.parent = self
        self.mode = mode
        self.list = []
    def eval(self):
        if self.mode == 0:
            return [arg for arg in self.args.eval()]
        else:
            return self.list
    def typecheck(self):
        if self.mode == 0:
            return self.args.typecheck()
        else:
            return True
def getWrapper(value):
    if isinstance(value, int):
        return Int(value)
    elif isinstance(value, str):
        temp_str = Str()
        temp_str.val = value
        return temp_str
    elif isinstance(value, float):
        return Real(value)
    elif isinstance(value, list):
        lst = List(Args(), 1)
        lst.list = value
        return lst
    elif isinstance(value, tuple):
        tple = Tuple(Args(), 1)
        tple.tuple = value
        return tple
# Logic ASTNodes.Nodes
class Negation(ASTNodes.Node):
    def __init__(self, child):
        super().__init__()
        self.child = child
        self.child.parent = self

    def eval(self):
        if self.child.eval() is None: 
            return False
        return not self.child.eval()

    def typecheck(self):
        if(self.child.typecheck()):
            if(isinstance(self.child.eval(), bool)):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False

class Conjunction(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() and self.right.eval()

    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if(isinstance(self.left.eval(), bool) and isinstance(self.right.eval(), bool)):
                    return True
            else:
                print("SEMANTIC ERROR")
                return False
        else:
            return False

class Disjunction(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() or self.right.eval()

    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if(isinstance(self.left.eval(), bool) and isinstance(self.right.eval(), bool)):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        else:
            return False
#Mathematical ASTNodes.Nodes
class Multiply(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() * self.right.eval()

    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number) or self.left.eval() is None)):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False

class Divide(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() / self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number) or self.left.eval() is None)):
                if(self.right.eval() != 0):
                    return True
            print("SEMANTIC ERROR")
            return False
        return False

class IntDivide(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() // self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), int) or self.right.eval() is None) and (isinstance(self.left.eval(), int) or self.left.eval() is None)):
                if(self.right.eval() != 0):
                    return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False

class Add(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() + self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number) or self.left.eval() is None)
                    or ((isinstance(self.right.eval(), str) or self.right.eval() is None) and (isinstance(self.left.eval(), str) or self.left.eval() is None))
                    or ((isinstance(self.right.eval(), list) or self.right.eval() is None) and (isinstance(self.left.eval(), list) or self.left.eval() is None))):
                        return True
            print("SEMANTIC ERROR")
            return False
        return False

class Sub(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() - self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number) or self.left.eval() is None)):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False
class Exp(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() ** self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number) or self.left.eval() is None)):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False

class Mod(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval() % self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), int) or self.right.eval() is None) and (isinstance(self.left.eval(), int) or self.left.eval() is None)):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False

class Membership(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return []
        return self.left.eval() in self.right.eval()
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if(isinstance(self.right.eval(), list) or (isinstance(self.right.eval(), str) or (self.right.eval() is None) and isinstance(self.left.eval(), str)) or self.left.eval() is None):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False

class Cons(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return []
        clone = copy.deepcopy(self.right.eval())
        clone.insert(0, self.left.eval())
        return clone
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if(isinstance(self.right.eval(), list) or self.right.eval() is None):
                return True
            else:
                print("SEMANTIC ERROR")
                return False
        return False
#Comparison ASTNodes.Nodes
class Compare(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if( ((isinstance(self.right.eval(), str) or self.right.eval() is None) and (isinstance(self.left.eval(), str) or self.left.eval() is None)) or 
            ((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number) or self.left.eval() is None) )):
                    return True
            print("SEMANTIC ERROR")
            return False
        return False
class Equivalency(Compare):
    def __init__(self, left, right):
        super().__init__(left, right)
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if( ((isinstance(self.right.eval(), str) or self.right.eval() is None) and (isinstance(self.left.eval(), str)) or self.left.eval() is None) or 
            ((isinstance(self.right.eval(), numbers.Number) or self.right.eval() is None) and (isinstance(self.left.eval(), numbers.Number)) or self.left.eval() is None) or 
            ((isinstance(self.right.eval(), bool)or self.right.eval() is None) and (isinstance(self.left.eval(), bool)or self.left.eval() is None))):
                    return True
            print("SEMANTIC ERROR")
            return False
        return False

class LessThan(Compare):
    def __init__(self, left, right):
        super().__init__(left, right)
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() < self.right.eval()
class LessEqual(Compare):
    def __init__(self, left, right):
        super().__init__(left, right)
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() <= self.right.eval()
class GreatThan(Compare):
    def __init__(self, left, right):
        super().__init__(left, right)
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() > self.right.eval()
class GreatEqual(Compare):
    def __init__(self, left, right):
        super().__init__(left, right)
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() >= self.right.eval()
class Equal(Equivalency):
    def __init__(self, left, right):
        super().__init__(left, right)
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() == self.right.eval()
class NotEqual(Equivalency):
    def __init__(self, left, right):
        super().__init__(left, right)
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return False
        return self.left.eval() != self.right.eval()
# Indexing Classes
class IndexTuple(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.right.eval()[self.left.eval() - 1]
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), tuple)or self.right.eval() is None) and (isinstance(self.left.eval(), int)or self.left.eval() is None)):
                if(self.left.eval() >= 1 and self.left.eval() <= len(self.right.eval())):
                    return True
            print("SEMANTIC ERROR")
            return False
        return False
class IndexList(ASTNodes.Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self
    def eval(self):
        if self.right.eval() is None or self.left.eval() is None:
            return 0
        return self.left.eval()[self.right.eval()]
    def typecheck(self):
        if(self.left.typecheck() and self.right.typecheck()):
            if((isinstance(self.right.eval(), int)or self.right.eval() is None) and ((isinstance(self.left.eval(), list) or self.left.eval() is None)
                            or ((isinstance(self.left.eval(), str) or self.left.eval() is None) and (isinstance(self.right.eval(), int) or self.right.eval() is None)))):
                if(self.right.eval() >= 0 and self.right.eval() < len(self.left.eval())):
                    return True
            print("SEMANTIC ERROR")
            return False
        return False

#token names
tokens = (  'LPAREN','RPAREN', 'COMMA',
            'RBRACK', 'LBRACK', 'MULT',
            'EXP', 'DIV', 'INTDIV', 'ADD',
            'SUB', 'MOD', 'MEM', 'CONS',
            'NEG', 'AND', 'OR', 'LESS', 'LESSEQ',
            'EQUAL', 'NOTEQ', 'GTR', 'GTREQ',
            'INT', 'REAL', 'BOOL', 'STR', 'SUBN', 'HASH',
            'SEMICOLON', 'VARIABLE', 'PRINT', 'SET',
            'WHILE', 'IF', 'ELSE', 'LBRACE', 'RBRACE',
            'FUNCTION')
#tokens
#Language 
t_VARIABLE = r'[a-zA-Z][a-zA-Z0-9_]*'
t_SEMICOLON = r'\s*;\s*'
t_SET = r'\s*=\s*'
#Expressions
t_COMMA = r'\s*\,\s*'
t_RPAREN = r'\s*\)\s*'
t_LPAREN = r'\s*\(\s*'
t_RBRACK = r'\s*\]\s*'
t_LBRACK = r'\s*\[\s*'
t_LBRACE = r'\s*{\s*'
t_RBRACE = r'\s*}\s*'
#Operators
t_MULT = r'\s*\*\s*'
t_EXP = r'\s*\*\*\s*'
t_DIV = r'\s*\/\s*'
t_ADD = r'\s*\+\s*'
t_SUB = r'\s*\-\s*'
t_SUBN = r'\s*\-'
t_CONS = r'\s*::\s*'
t_HASH = r'\s*\#\s*'
#Comparators
t_LESS = r'\s*<\s*'
t_LESSEQ = r'\s*<=\s*'
t_EQUAL = r'\s*==\s*'
t_NOTEQ = r'\s*<>\s*'
t_GTR = r'\s*>\s*'
t_GTREQ = r'\s*>=\s*'
#token function
def t_FUNCTION(t):
    r'\s*fun\s*'
    return t

def t_WHILE(t):
    r'while\s*\(\s*'
    return t
def t_IF(t):
    r'if\s*\(\s*'
    return t
def t_ELSE(t):
    r'\s*else\s*'
    return t
def t_PRINT(t):
    r'print\s*\(\s*'
    return t
def t_REAL(t):
    r'((\d+\.\d*)|(\d*\.\d+))(e-?\d+)?'
    return t
def t_INT(t):
    r'\d+' 
    return t
def t_BOOL(t):
    r'(True|False)'
    return t
def t_STR(t):
    r'(\"[^\"]*\")|(\'[^\']*\')'
    return t
def t_AND(t):
    r'\s*andalso\s*'
    return t
def t_INTDIV(t):
    r'\s*div\s*'
    return t
def t_MEM(t):
    r'\s*\sin\s\s*'
    return t
def t_MOD(t):
    r'\s*mod\s*'
    return t
def t_OR(t):
    r'\s*orelse\s*'
    return t
def t_NEG(t):
    r'\s*not\s*'
    return t
#ignore tokens
t_ignore = ' \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

#token errors
def t_error(t):
    # print("Illegal Character '%s', at %d, %d" %
    #       (t.value[0], t.lineno, t.lexpos))
    print("SYNTAX ERROR")

    if not debug_jason:
        raise ValueError()
    # print("I AM PRINTING MORE THAN ONCE")
    t.lexer.skip(1)

# Build lexer
import ply.lex as lex
lexer = lex.lex(debug = False)

def tokenize(inp):
    lexer.input(inp)
    while True:
        tok = lexer.token()
        if not tok:
            break
#defining productions
names = {}
precedence = (('left', 'OR'), ('left', 'AND'), ('left', 'NEG'),
              ('left', 'GTR', 'GTREQ', 'LESS', 'LESSEQ', 'NOTEQ', 'EQUAL'),
              ('right', 'CONS'),
              ('left', 'MEM'),
              ('left', 'ADD', 'SUB'),
              ('left', 'MULT', 'DIV', 'MOD', 'INTDIV'),
              ('right', 'EXP'),
              ('left', 'LISTINDEX', 'LBRACK', 'RBRACK'),
              ('left', 'SET'),
              ('left', 'TUPLEINDEX'))
def p_eval_smt(p):
    'eval : smts'
    for smt in p[1]:
        if(not smt.typecheck()):
            raise ValueError()
    for smt in p[1]:
        smt.eval()
def p_block_smts(p):
    'smt : LBRACE smts RBRACE'
    p[0] = ASTNodes.Block(p[2])
def p_while_smts(p):
    'smt : WHILE expr RPAREN smt'
    p[0] = ASTNodes.While(p[2], p[4])
def p_ifelse_smts(p):
    'smt : IF expr RPAREN smt ELSE smt'
    p[0] = ASTNodes.IfElse(p[2], p[4], p[6])
def p_if_smts(p):
    'smt : IF expr RPAREN smt'
    p[0] = ASTNodes.If(p[2], p[4])
def p_smts_empty(p):
    'smts :'
    p[0] = []
def p_smts_smt(p):
    'smts : smt smts'
    p[0] = [p[1]] + p[2]
def p_smt_print(p):
    'smt : PRINT expr RPAREN SEMICOLON'
    p[0] = ASTNodes.Print(p[2])
def p_smt_set(p):
    'smt : var SET expr SEMICOLON'
    p[0] = ASTNodes.Set(p[3], p[1])
def p_expr_var(p):
    'expr : var'
    p[0] = p[1]
def p_var(p):
    'var : VARIABLE'
    p[0] = ASTNodes.Variable(p[1])
def p_var_index(p):
    'var : var LBRACK expr RBRACK'
    if(p[1].typecheck()):
        p[0] = ASTNodes.Variable(p[3], p[1])
    else: 
        raise ValueError()
def p_funct_name(p):
    'functDef : FUNCTION VARIABLE LPAREN '
    ASTNodes.functDict[p[2]] = None
    p[0] = p[2]
def p_funct_define(p):
    'smt : functDef variables RPAREN SET smt expr SEMICOLON'
    p[0] = ASTNodes.Funct(p[1], p[2], p[5], p[6])

def p_variables_empty(p):
    'variables :'
    p[0] = []
def p_variables(p):
    'variables : VARIABLE COMMA variables'
    ASTNodes.varDict[p[1]] = None
    p[0] = [p[1]] + p[3]
def p_variables_single(p):
    'variables : VARIABLE'
    ASTNodes.varDict[p[1]] = None
    p[0] = [p[1]]
#Expression Productions
def p_funct_exec(p):
    'expr : VARIABLE LPAREN args RPAREN'
    p[0] = ASTNodes.FunctExec(p[1], p[3])
    
def p_num_int(p):
    'num : INT'
    p[0] = Int(p[1])
def p_exp_str(p):
    'expr : STR'
    p[0] = Str(p[1])
def p_exp_bool(p):
    'expr : BOOL'
    p[0] = Bool(p[1])
def p_exp_real(p):
    'num : REAL'
    p[0] = Real(p[1])
def p_expr_num(p):
    '''expr : num
            | SUBN num'''
    if len(p) < 3:
        p[0] = p[1]
    else:
        p[2].val = '-' + p[2].val
        p[0] = p[2]
def p_index_tuple(p):
    'expr : HASH expr tuple %prec TUPLEINDEX'
    p[0] = IndexTuple(p[2], p[3])
    if(p[0].typecheck()):
        p[0] = getWrapper(p[0].eval())
    else:    
        raise ValueError()
def p_index_tuple_expr(p):
    'expr : HASH expr expr'
    p[0] = IndexTuple(p[2], p[3])
    if(p[0].typecheck()):
        p[0] = getWrapper(p[0].eval())
    else:    
        raise ValueError()
    
def p_index_list(p):
    'expr : expr LBRACK expr RBRACK %prec LISTINDEX'
    p[0] = IndexList(p[1], p[3])
    # if(p[0].typecheck()):
    #     p[0] = getWrapper(p[0].eval())
    # else:    
    #     raise ValueError()
def p_expr_list(p):
    'expr : list'
    p[0] = p[1]
def p_expr_tuple(p):
    'expr : tuple'
    p[0] = p[1]

def p_expr_paren(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_div(p): 
    'expr : expr DIV expr'
    p[0] = Divide(p[1], p[3])
def p_expr_intdiv(p):
    'expr : expr INTDIV expr'
    p[0] = IntDivide(p[1], p[3])
def p_expr_mult(p):
    'expr : expr MULT expr'
    p[0] = Multiply(p[1], p[3])
def p_expr_add(p):
    'expr : expr ADD expr'
    p[0] = Add(p[1], p[3])
def p_expr_sub(p):
    'expr : expr SUB expr'
    p[0] = Sub(p[1], p[3])
def p_expr_mod(p):
    'expr : expr MOD expr'
    p[0] = Mod(p[1], p[3])
def p_expr_exp(p):
    'expr : expr EXP expr'
    p[0] = Exp(p[1], p[3])
def p_expr_mem(p):
    'expr : expr MEM expr'
    p[0] = Membership(p[1], p[3])
def p_expr_cons(p):
    'expr : expr CONS expr'
    p[0] = Cons(p[1], p[3])
def p_expr_neg(p):
    'expr : NEG expr'
    p[0] = Negation(p[2])
def p_expr_and(p):
    'expr : expr AND expr'
    p[0] = Conjunction(p[1], p[3])
def p_expr_or(p):
    'expr : expr OR expr'
    p[0] = Disjunction(p[1], p[3])
def p_expr_less(p):
    'expr : expr LESS expr'
    p[0] = LessThan(p[1], p[3])

def p_expr_lesseq(p):
    'expr : expr LESSEQ expr'
    p[0] = LessEqual(p[1], p[3])
def p_expr_equal(p):
    'expr : expr EQUAL expr'
    p[0] = Equal(p[1], p[3])
def p_expr_noteq(p):
    'expr : expr NOTEQ expr'
    p[0] = NotEqual(p[1], p[3])
def p_expr_gtreq(p):
    'expr : expr GTREQ expr'
    p[0] = GreatEqual(p[1], p[3])
def p_expr_gtr(p):
    'expr : expr GTR expr'
    p[0] = GreatThan(p[1], p[3])


#List
def p_list(p):
    'list : LBRACK args RBRACK'
    p[0] = List(p[2])
def p_list_empty(p):
    'list : LBRACK RBRACK'
    p[0] = List()
#Tuple
def p_tuple(p):
    'tuple : LPAREN args RPAREN'
    p[0] = Tuple(p[2])
def p_tuple_empty(p):
    'tuple : LPAREN RPAREN'
    p[0] = Tuple()
#Args productions
def p_argsComma(p):
    'args : args COMMA'
    p[0] = Args()
    p[0].merge_args(p[1].get_args())
def p_args(p):
    'args : args COMMA expr'
    p[0] = Args()
    p[0].merge_args(p[1].get_args())
    p[0].add_arg(p[3])
def p_args_operands(p):
    '''args : expr'''
    p[0] = Args()
    p[0].add_arg(p[1])

def p_error(p):
    print("SYNTAX ERROR")
    if not debug_jason:
        raise ValueError()
    else:
        print("Syntax error at '%s' (%d, %d)" % (p.value, p.lineno, p.lexpos))
import ply.yacc as yacc
parser = yacc.yacc(debug = False)
def parse(inp):
    result = parser.parse(inp, debug=0)
    return result

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2 :
        exit(0)
    debug_jason = False
    filename = sys.argv[1]
    if filename:
        with open(filename, "r") as fp:
            blocks = ""
            for line in fp:
                blocks += line
            try:
                parse(blocks)
            except ValueError as e:
                if debug_jason:
                    pass
                else:
                    pass
    exit(0)