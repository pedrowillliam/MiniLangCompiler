from src.ast_node import *
from src.tabela_simbolos import TabelaSimbolos

class AnalisadorSemantico:
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.tipo_retorno_atual = None

    def semantic_error(self, node, msg):
        linha = "desconhecida"
        if hasattr(node, 'token'): # Para IdentifierNode, NumeroIntNode...
            linha = node.token.line
        elif hasattr(node, 'op'):    # Para BinOpNode, UnaryOpNode...
            linha = node.op.line
        elif hasattr(node, 'id_node'): # Para AssignNode...
            linha = node.id_node.token.line
            
        raise Exception(f"Erro Semântico na linha {linha}: {msg}")

    def analisar(self, node):
        """Método genérico que despacha a visita para o método correto."""
        metodo_nome = f'visit_{type(node).__name__}'
        visitante = getattr(self, metodo_nome, self.generic_visit)
        return visitante(node)

    def generic_visit(self, node):
        raise Exception(f"Nenhum método visit_{type(node).__name__} implementado.")

    # --- VISITAÇÃO DE ESTRUTURAS ---

    def visit_ProgramNode(self, node):
        self.analisar(node.block)

    def visit_BlockNode(self, node):
        # 1. Processa declarações de variáveis
        for var_decl in node.vars_decl:
            self.analisar(var_decl)
        
        # 2. Processa sub-rotinas (funções/procedimentos)
        for sub in node.subroutines:
            self.analisar(sub)
            
        # 3. Processa comandos do corpo
        for cmd in node.comandos:
            self.analisar(cmd)

    def visit_VarDeclNode(self, node):
        for id_node in node.id_nodes:
            nome = id_node.name
            # Verifica se já existe no escopo atual
            if nome in self.tabela.pilha_escopos[-1]:
                self.semantic_error(id_node, f"Variável '{nome}' já declarada neste escopo.")
            
            if node.type_name == 'void':
                self.semantic_error(id_node, "Variáveis não podem ser do tipo 'void'.")
                
            self.tabela.declarar(nome, 'variavel', node.type_name)

    # --- VISITAÇÃO DE COMANDOS ---

    def visit_AssignNode(self, node):
        nome = node.id_node.name
        simbolo = self.tabela.buscar(nome)
        
        if not simbolo:
            self.semantic_error(node.id_node, f"Variável '{nome}' não declarada.")
        
        if simbolo.categoria != 'variavel':
            self.semantic_error(node.id_node, f"'{nome}' não é uma variável atribuível.")

        tipo_expr = self.analisar(node.expr)

        # TIPAGEM FORTE: Não permite atribuição entre tipos diferentes, mesmo que sejam compatíveis (ex: int para float)
        if simbolo.tipo != tipo_expr:
            self.semantic_error(node.id_node, f"Atribuição inválida. Variável '{nome}' é '{simbolo.tipo}', mas recebeu '{tipo_expr}'.")

    # --- VISITAÇÃO DE EXPRESSÕES (Onde a mágica acontece) ---

    def visit_BinOpNode(self, node):
        tipo_esq = self.analisar(node.left)
        tipo_dir = self.analisar(node.right)
        op = node.op.value

        if op in ['+', '-', '*', '/']:
            if tipo_esq not in ['inteiro', 'float'] or tipo_dir not in ['inteiro', 'float']:
                self.semantic_error(node, f"Operador '{op}' exige tipos numéricos.")
            if tipo_esq != tipo_dir:
                self.semantic_error(node, f"Tipagem forte: Não pode operar '{tipo_esq}' com '{tipo_dir}'.")
            return tipo_esq 

        # Operações Relacionais (Retornam booleano)
        if op in ['>', '<', '==', '!=', '>=', '<=']:
            if tipo_esq != tipo_dir:
                 self.semantic_error(node, f"Não é possível comparar tipos diferentes: '{tipo_esq}' {op} '{tipo_dir}'.")
            return 'booleano'

        # Operações Lógicas 
        if op in ['e', 'ou']:
            if tipo_esq != 'booleano' or tipo_dir != 'booleano':
                self.semantic_error(node, f"Operador lógico '{op}' exige operandos booleanos.")
            return 'booleano'

        return None
    
    def visit_UnaryOpNode(self, node):
        tipo_expr = self.analisar(node.expr)
        op = node.op.value

        if op in ['+', '-']:
            if tipo_expr not in ['inteiro', 'float']:
                self.semantic_error(node, f"Operador unário '{op}' exige tipo numérico, mas recebeu '{tipo_expr}'.")
            return tipo_expr
            
        if op == 'nao':
            if tipo_expr != 'booleano':
                self.semantic_error(node, f"Operador 'nao' exige tipo booleano, mas recebeu '{tipo_expr}'.")
            return 'booleano'

        return None

    def visit_IdentifierNode(self, node):
        simbolo = self.tabela.buscar(node.name)
        if not simbolo:
            self.semantic_error(node, f"Identificador '{node.name}' não declarado.")
        return simbolo.tipo

    def visit_NumeroIntNode(self, node):
        return 'inteiro'

    def visit_NumeroFloatNode(self, node):
        return 'float'

    def visit_BooleanoNode(self, node):
        return 'booleano'
    
    def visit_LiteralCharNode(self, node):
        return 'char'
    
# --- CONTROLE DE FLUXO ---

    def visit_IfNode(self, node):
        tipo_cond = self.analisar(node.condition)
        if tipo_cond != 'booleano':
            self.semantic_error(node.condition, "A condição do 'se' deve ser booleana.")
        
        self.analisar(node.true_block)
        if node.false_block:
            self.analisar(node.false_block)

    def visit_WhileNode(self, node):
        tipo_cond = self.analisar(node.condition)
        if tipo_cond != 'booleano':
            self.semantic_error(node.condition, "A condição do 'enquanto' deve ser booleana.")
        self.analisar(node.body)

    # --- SUB-ROTINAS (FUNÇÕES E PROCEDIMENTOS) ---

    def visit_SubroutineNode(self, node):
        # 1. Registra na tabela (precisa ser feito antes de entrar no bloco)
        tipos_params = [p.type_name for p in node.params]
        # Aqui você usa o seu método de declarar na tabela
        self.tabela.declarar(node.name, 'funcao', node.return_type, tipos_params)

        # 2. Entra no escopo da função
        self.tabela.entrar_escopo()
        
        # 3. Define o retorno esperado para validar o 'retorne' lá dentro
        old_retorno = self.tipo_retorno_atual
        self.tipo_retorno_atual = node.return_type

        # 4. Declara os parâmetros como variáveis locais
        for p in node.params:
            self.tabela.declarar(p.id_node.name, 'variavel', p.type_name)

        # 5. Analisa o bloco da função
        self.analisar(node.block)

        # 6. Sai do escopo e restaura estado
        self.tabela.sair_escopo()
        self.tipo_retorno_atual = old_retorno

    def visit_ReturnNode(self, node):
        tipo_ret = 'void'
        if node.expr:
            tipo_ret = self.analisar(node.expr)
        
        if tipo_ret != self.tipo_retorno_atual:
            self.semantic_error(node, f"Retorno inválido. Esperava '{self.tipo_retorno_atual}', mas retornou '{tipo_ret}'.")

    def visit_FunctionCallNode(self, node):
        nome = node.id_node.name
        simbolo = self.tabela.buscar(nome)
        
        if not simbolo or simbolo.categoria != 'funcao':
            self.semantic_error(node.id_node, f"'{nome}' não é uma função.")

        # Valida argumentos
        args_analisados = [self.analisar(arg) for arg in node.args]
        if len(args_analisados) != len(simbolo.params):
            self.semantic_error(node.id_node, f"Função '{nome}' espera {len(simbolo.params)} argumentos, recebeu {len(args_analisados)}.")

        for i, (tipo_arg, tipo_param) in enumerate(zip(args_analisados, simbolo.params)):
            if tipo_arg != tipo_param:
                self.semantic_error(node.id_node, f"Argumento {i+1} de '{nome}' deve ser '{tipo_param}', mas é '{tipo_arg}'.")
        
        return simbolo.tipo

    # --- EXTRAS ---
    def visit_PrintNode(self, node):
        self.analisar(node.expr)

    def visit_BreakNode(self, node):
        pass # Poderia validar se está dentro de um While no futuro

    def visit_ContinueNode(self, node):
        pass