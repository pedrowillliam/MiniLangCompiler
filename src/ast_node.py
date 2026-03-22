class AST:
    pass

# --- NÓS DE VALORES BÁSICOS ---
class NumeroIntNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = int(token.value)

class NumeroFloatNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = float(token.value)

class LiteralCharNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BooleanoNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = True if token.value == 'verdadeiro' else False

class IdentifierNode(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

# --- NÓS DE EXPRESSÕES ---
class BinOpNode(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op          # O token do operador (+, -, *, /, >, ==)
        self.right = right

class UnaryOpNode(AST):
    def __init__(self, op, expr):
        self.op = op          # O token do operador unário (+, -, nao)
        self.expr = expr

# --- NÓS DE COMANDOS E FLUXO ---
class AssignNode(AST):
    def __init__(self, id_node, expr):
        self.id_node = id_node # IdentifierNode
        self.expr = expr       # Nó da expressão

class IfNode(AST):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition     # Nó da expressão booleana
        self.true_block = true_block   # Nó de comando do 'entao'
        self.false_block = false_block # Nó de comando do 'senao' (opcional)

class WhileNode(AST):
    def __init__(self, condition, body):
        self.condition = condition # Nó da expressão booleana
        self.body = body           # Nó de comando do 'faca'

class FunctionCallNode(AST):
    def __init__(self, id_node, args):
        self.id_node = id_node # IdentifierNode (nome da função)
        self.args = args       # Lista de nós de expressão

class PrintNode(AST):
    def __init__(self, expr):
        self.expr = expr # Nó de expressão a ser impressa

class ReturnNode(AST):
    def __init__(self, expr=None):
        self.expr = expr # Nó de expressão a ser retornada (opcional)

class BreakNode(AST):
    def __init__(self, token):
        self.token = token

class ContinueNode(AST):
    def __init__(self, token):
        self.token = token

# --- NÓS DE DECLARAÇÕES E ESTRUTURA ---
class VarDeclNode(AST):
    def __init__(self, id_nodes, type_name):
        self.id_nodes = id_nodes   # Lista de IdentifierNode (ex: var x, y)
        self.type_name = type_name # String ('inteiro', 'float', etc)

class ParamNode(AST):
    def __init__(self, id_node, type_name):
        self.id_node = id_node     # IdentifierNode
        self.type_name = type_name # String ('inteiro', etc)

class SubroutineNode(AST):
    # Serve tanto para 'funcao' quanto para 'procedimento'
    def __init__(self, is_function, name, params, return_type, block):
        self.is_function = is_function # Booleano: True=funcao, False=procedimento
        self.name = name               # String (nome da rotina)
        self.params = params           # Lista de ParamNode
        self.return_type = return_type # String ('void', 'inteiro', etc)
        self.block = block             # BlockNode com o corpo

class BlockNode(AST):
    def __init__(self, vars_decl, subroutines, comandos):
        self.vars_decl = vars_decl     # Lista de VarDeclNode
        self.subroutines = subroutines # Lista de SubroutineNode
        self.comandos = comandos       # Lista de nós de comandos (AssignNode, IfNode...)

class ProgramNode(AST):
    def __init__(self, name, block):
        self.name = name   # String com o nome do programa
        self.block = block # BlockNode