from src.ast_node import *

class ASTPrinter:
    def imprimir(self, node, nivel=0):
        if node is None:
            return
            
        indent = "  " * nivel
        nome_classe = node.__class__.__name__

        if isinstance(node, ProgramNode):
            print(f"{indent}└── {nome_classe} (Nome: {node.name})")
            self.imprimir(node.block, nivel + 1)
            
        elif isinstance(node, BlockNode):
            print(f"{indent}└── {nome_classe}")
            for var in node.vars_decl: self.imprimir(var, nivel + 1)
            for sub in node.subroutines: self.imprimir(sub, nivel + 1)
            for cmd in node.comandos: self.imprimir(cmd, nivel + 1)
            
        elif isinstance(node, VarDeclNode):
            ids = ", ".join([n.name for n in node.id_nodes])
            print(f"{indent}└── {nome_classe} (Tipo: {node.type_name}, IDs: {ids})")
            
        elif isinstance(node, SubroutineNode):
            tipo = "Funcao" if node.is_function else "Procedimento"
            print(f"{indent}└── {nome_classe} ({tipo}: {node.name}, Retorno: {node.return_type})")
            for p in node.params:
                print(f"{indent}      Param: {p.id_node.name} ({p.type_name})")
            self.imprimir(node.block, nivel + 1)
            
        elif isinstance(node, AssignNode):
            print(f"{indent}└── {nome_classe}")
            self.imprimir(node.id_node, nivel + 1)
            self.imprimir(node.expr, nivel + 1)
            
        elif isinstance(node, BinOpNode):
            print(f"{indent}└── {nome_classe} (Operador: {node.op.value})")
            self.imprimir(node.left, nivel + 1)
            self.imprimir(node.right, nivel + 1)
            
        elif isinstance(node, UnaryOpNode):
            print(f"{indent}└── {nome_classe} (Operador: {node.op.value})")
            self.imprimir(node.expr, nivel + 1)
            
        elif isinstance(node, IfNode):
            print(f"{indent}└── {nome_classe}")
            print(f"{indent}    [Condicao]")
            self.imprimir(node.condition, nivel + 2)
            print(f"{indent}    [Entao]")
            self.imprimir(node.true_block, nivel + 2)
            if node.false_block:
                print(f"{indent}    [Senao]")
                self.imprimir(node.false_block, nivel + 2)
                
        elif isinstance(node, WhileNode):
            print(f"{indent}└── {nome_classe}")
            print(f"{indent}    [Condicao]")
            self.imprimir(node.condition, nivel + 2)
            print(f"{indent}    [Faca]")
            self.imprimir(node.body, nivel + 2)
            
        elif isinstance(node, PrintNode):
            print(f"{indent}└── {nome_classe}")
            self.imprimir(node.expr, nivel + 1)
            
        elif isinstance(node, ReturnNode):
            print(f"{indent}└── {nome_classe}")
            if node.expr: self.imprimir(node.expr, nivel + 1)
            
        elif isinstance(node, FunctionCallNode):
            print(f"{indent}└── {nome_classe} (Chamada: {node.id_node.name})")
            for arg in node.args:
                self.imprimir(arg, nivel + 1)
                
        elif isinstance(node, IdentifierNode):
            print(f"{indent}└── {nome_classe} ('{node.name}')")
            
        elif isinstance(node, (NumeroIntNode, NumeroFloatNode, BooleanoNode, LiteralCharNode)):
            print(f"{indent}└── {nome_classe} ({node.value})")
            
        elif isinstance(node, (BreakNode, ContinueNode)):
            print(f"{indent}└── {nome_classe}")
            
        else:
            print(f"{indent}└── {nome_classe} (Nó não detalhado no impressor)")