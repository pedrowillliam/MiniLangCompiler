from src.ast_node import *

class ParserTopDown:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self, msg):
        raise SyntaxError(f"Erro Sintático na linha {self.current_token.line}: {msg}. Encontrado: '{self.current_token.value}'")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.error(f"Esperava token do tipo {token_type}")

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    # --- Regras da Gramática (Montando a AST) ---
    def parse_programa(self):
        print(f"-> Iniciando análise do Programa...")
        self.eat('PROGRAMA')
        nome_programa = self.current_token.value
        self.eat('ID') 
        
        bloco_node = self.parse_bloco()
        
        if self.current_token.type != 'EOF':
            self.error("Código extra encontrado após o fim do programa")
            
        print("<- Árvore Sintática (AST) gerada com sucesso!")
        return ProgramNode(nome_programa, bloco_node)

    def parse_bloco(self):
        vars_decl = []
        subrotinas = []
        comandos = []

        while self.current_token.type == 'VAR':
            vars_decl.append(self.parse_decl_var())
            
        while self.current_token.type in ('PROCEDIMENTO', 'FUNCAO'):
            subrotinas.append(self.parse_decl_subrotina())
            
        comandos = self.parse_corpo()
        
        return BlockNode(vars_decl, subrotinas, comandos)

    def parse_decl_var(self):
        self.eat('VAR')
        id_nodes = self.parse_lista_ids() 
        tipo = self.parse_tipo()      
        self.eat('PONTO_VIRG')
        
        return VarDeclNode(id_nodes, tipo)

    def parse_lista_ids(self):
        ids = []
        ids.append(IdentifierNode(self.current_token))
        self.eat('ID')
        while self.current_token.type == 'ID':
            ids.append(IdentifierNode(self.current_token))
            self.eat('ID')
        return ids

    def parse_tipo(self):
        if self.current_token.type in ['INTEIRO', 'FLOAT', 'BOOLEANO', 'CHAR', 'VOID']:
            tipo = self.current_token.type.lower()
            self.eat(self.current_token.type)
            return tipo
        else:
            self.error("Esperado tipo (inteiro, float, booleano, char ou void)")

    def parse_decl_subrotina(self):
        if self.current_token.type == 'PROCEDIMENTO':
            return self.parse_decl_procedimento()
        elif self.current_token.type == 'FUNCAO':
            return self.parse_decl_funcao()

    def parse_decl_procedimento(self):
        self.eat('PROCEDIMENTO')
        nome = self.current_token.value
        self.eat('ID')
        self.eat('ABRE_PAR')
        params = self.parse_lista_params()
        self.eat('FECHA_PAR')
        bloco = self.parse_bloco()
        self.eat('PONTO_VIRG')
        
        return SubroutineNode(is_function=False, name=nome, params=params, return_type='void', block=bloco)

    def parse_decl_funcao(self):
        self.eat('FUNCAO')
        nome = self.current_token.value
        self.eat('ID')
        self.eat('ABRE_PAR')
        params = self.parse_lista_params()
        self.eat('FECHA_PAR')
        self.eat('DOIS_PONTOS')
        tipo_retorno = self.parse_tipo()
        bloco = self.parse_bloco()
        self.eat('PONTO_VIRG')
        
        return SubroutineNode(is_function=True, name=nome, params=params, return_type=tipo_retorno, block=bloco)

    def parse_lista_params(self):
        params = []
        if self.current_token.type == 'ID':
            params.append(self.parse_param())
            while self.current_token.type == 'ID':
                params.append(self.parse_param())
        return params

    def parse_param(self):
        id_node = IdentifierNode(self.current_token)
        self.eat('ID')
        tipo = self.parse_tipo()
        return ParamNode(id_node, tipo)

    def parse_corpo(self):
        comandos = []
        self.eat('INICIO')
        while self.current_token.type != 'FIM':
            comandos.append(self.parse_comando())
            self.eat('PONTO_VIRG')
        self.eat('FIM')
        return comandos

    def parse_comando(self):
        tok = self.current_token.type
        if tok == 'INICIO':
            comandos = self.parse_corpo()
            # Um bloco interno de comandos retorna um BlockNode simplificado (sem var/func)
            return BlockNode([], [], comandos)
        elif tok == 'SE':
            return self.parse_se()
        elif tok == 'ENQUANTO':
            return self.parse_enquanto()
        elif tok == 'RETORNE':
            return self.parse_retorne()
        elif tok == 'BREAK':
            token = self.current_token
            self.eat('BREAK')
            return BreakNode(token)
        elif tok == 'CONTINUE':
            token = self.current_token
            self.eat('CONTINUE')
            return ContinueNode(token)
        elif tok == 'ESCREVA':
            return self.parse_escreva()
        elif tok == 'ID':
            proximo = self.peek()
            if proximo and proximo.type == 'DOIS_PONTOS':
                return self.parse_atribuicao()
            elif proximo and proximo.type == 'ABRE_PAR':
                return self.parse_chamada_subrotina()
            else:
                self.error("Esperado ':' ou '(' após ID")
        else:
            self.error("Comando inválido")

    def parse_atribuicao(self):
        id_token = self.current_token
        self.eat('ID')
        self.eat('DOIS_PONTOS')
        expr_node = self.parse_expressao()
        
        return AssignNode(IdentifierNode(id_token), expr_node)

    def parse_chamada_subrotina(self):
        id_token = self.current_token
        self.eat('ID')
        self.eat('ABRE_PAR')
        args = self.parse_lista_exp()
        self.eat('FECHA_PAR')
        
        return FunctionCallNode(IdentifierNode(id_token), args)

    def parse_se(self):
        self.eat('SE')
        self.eat('ABRE_PAR')
        cond_node = self.parse_expressao()
        self.eat('FECHA_PAR')
        self.eat('ENTAO')
        true_block = self.parse_comando()
        
        false_block = None
        if self.current_token.type == 'SENAO':
            self.eat('SENAO')
            false_block = self.parse_comando()
            
        return IfNode(cond_node, true_block, false_block)

    def parse_enquanto(self):
        self.eat('ENQUANTO')
        self.eat('ABRE_PAR')
        cond_node = self.parse_expressao()
        self.eat('FECHA_PAR')
        self.eat('FACA')
        body_block = self.parse_comando()
        
        return WhileNode(cond_node, body_block)

    def parse_retorne(self):
        self.eat('RETORNE')
        expr_node = None
        
        if self.current_token.type in ['ID', 'NUMERO', 'NUMERO_FLOAT', 'LITERAL_CHAR', 'NAO', 'ABRE_PAR', 'VERDADEIRO', 'FALSO', 'MAIS', 'MENOS']:
            expr_node = self.parse_expressao()
            
        return ReturnNode(expr_node)

    def parse_escreva(self):
        self.eat('ESCREVA')
        self.eat('ABRE_PAR')
        expr_node = self.parse_expressao()
        self.eat('FECHA_PAR')
        
        return PrintNode(expr_node)

    def parse_lista_exp(self):
        args = []
        if self.current_token.type != 'FECHA_PAR':
            args.append(self.parse_expressao())
            while self.current_token.type == 'VIRGULA':
                self.eat('VIRGULA')
                args.append(self.parse_expressao())
        return args

    def parse_expressao(self):
        esq_node = self.parse_expr_simples()
        
        if self.current_token.type in ['IGUAL', 'DIFERENTE', 'MAIOR', 'MENOR', 'MAIOR_IGUAL', 'MENOR_IGUAL']:
            op_token = self.current_token
            self.eat(op_token.type)
            dir_node = self.parse_expr_simples()
            return BinOpNode(esq_node, op_token, dir_node)
            
        return esq_node

    def parse_expr_simples(self):
        op_unario = None
        if self.current_token.type in ['MAIS', 'MENOS', 'NAO']:
            op_unario = self.current_token
            self.eat(op_unario.type)
            
        esq_node = self.parse_termo()
        
        if op_unario:
            esq_node = UnaryOpNode(op_unario, esq_node)
        
        while self.current_token.type in ['MAIS', 'MENOS', 'OU']:
            op_token = self.current_token
            self.eat(op_token.type)
            dir_node = self.parse_termo()
            esq_node = BinOpNode(esq_node, op_token, dir_node)
            
        return esq_node

    def parse_termo(self):
        esq_node = self.parse_fator()
        
        while self.current_token.type in ['VEZES', 'DIVIDIDO', 'E']:
            op_token = self.current_token
            self.eat(op_token.type)
            dir_node = self.parse_fator()
            esq_node = BinOpNode(esq_node, op_token, dir_node)
            
        return esq_node

    def parse_fator(self):
        tok = self.current_token
        if tok.type == 'ID':
            if self.peek() and self.peek().type == 'ABRE_PAR':
                return self.parse_chamada_subrotina() 
            else:
                self.eat('ID')
                return IdentifierNode(tok) 
                
        elif tok.type == 'NUMERO':
            self.eat('NUMERO')
            return NumeroIntNode(tok)
            
        elif tok.type == 'NUMERO_FLOAT':
            self.eat('NUMERO_FLOAT')
            return NumeroFloatNode(tok)
            
        elif tok.type == 'LITERAL_CHAR':
            self.eat('LITERAL_CHAR')
            return LiteralCharNode(tok)
            
        elif tok.type in ['VERDADEIRO', 'FALSO']:
            self.eat(tok.type)
            return BooleanoNode(tok)
            
        elif tok.type == 'ABRE_PAR':
            self.eat('ABRE_PAR')
            node = self.parse_expressao()
            self.eat('FECHA_PAR')
            return node
            
        else:
            self.error("Fator inválido")