from src.tabela_simbolos import TabelaSimbolos  

class ParserTopDown:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        
        self.tabela = TabelaSimbolos()
        self.tipo_retorno_atual = None 

    def error(self, msg):
        raise SyntaxError(f"Erro Sintático na linha {self.current_token.line}: {msg}. Encontrado: '{self.current_token.value}'")

    def semantic_error(self, msg):
        raise Exception(f"Erro Semântico na linha {self.current_token.line}: {msg}")

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

    # --- Funções Auxiliares de Semântica ---
    def declarar_simbolo(self, nome, categoria, tipo, params=None):
        """Verifica duplicação antes de declarar na tabela."""
        escopo_atual = self.tabela.pilha_escopos[-1]
        if nome in escopo_atual:
            self.semantic_error(f"O identificador '{nome}' já foi declarado neste escopo.")
        self.tabela.declarar(nome, categoria, tipo, params)

    def buscar_simbolo(self, nome):
        """Busca e lança erro se não existir."""
        simbolo = self.tabela.buscar(nome)
        if not simbolo:
            self.semantic_error(f"Variável ou função '{nome}' não declarada.")
        return simbolo

    # --- Regras da Gramática ---
    def parse_programa(self):
        print(f"-> Iniciando análise do Programa...")
        self.eat('PROGRAMA')
        self.eat('ID')
        self.parse_bloco()
        if self.current_token.type != 'EOF':
            self.error("Código extra encontrado após o fim do programa")
        print("<- Análise Sintática e Semântica concluídas com sucesso!")

    def parse_bloco(self):
        while self.current_token.type == 'VAR':
            self.parse_decl_var()
        while self.current_token.type in ('PROCEDIMENTO', 'FUNCAO'):
            self.parse_decl_subrotina()
        self.parse_corpo()

    def parse_decl_var(self):
        self.eat('VAR')
        ids = self.parse_lista_ids() 
        tipo = self.parse_tipo()      
        
        if tipo == 'void':
            self.semantic_error("Variáveis não podem ser do tipo 'void'.")
            
        self.eat('PONTO_VIRG')
        
        # SEMÂNTICO: Declara todas as variáveis da lista na tabela
        for nome_id in ids:
            self.declarar_simbolo(nome_id, 'variavel', tipo)

    def parse_lista_ids(self):
        ids = []
        ids.append(self.current_token.value)
        self.eat('ID')
        while self.current_token.type == 'ID':
            ids.append(self.current_token.value)
            self.eat('ID')
        return ids

    def parse_tipo(self):
        if self.current_token.type in ['INTEIRO', 'BOOLEANO', 'CHAR', 'VOID']:
            tipo = self.current_token.type.lower()
            self.eat(self.current_token.type)
            return tipo
        else:
            self.error("Esperado tipo (inteiro, booleano, char ou void)")

    def parse_decl_subrotina(self):
        if self.current_token.type == 'PROCEDIMENTO':
            self.parse_decl_procedimento()
        elif self.current_token.type == 'FUNCAO':
            self.parse_decl_funcao()

    def parse_decl_procedimento(self):
        self.eat('PROCEDIMENTO')
        nome = self.current_token.value
        self.eat('ID')
        self.eat('ABRE_PAR')
        params = self.parse_lista_params()
        self.eat('FECHA_PAR')
        
        # SEMÂNTICO: Registra o procedimento como uma função void
        tipos_params = [p['tipo'] for p in params]
        self.declarar_simbolo(nome, 'funcao', 'void', tipos_params)
        
        self.tabela.entrar_escopo()
        # Declara os parâmetros como variáveis locais
        for p in params:
            self.declarar_simbolo(p['nome'], 'variavel', p['tipo'])
            
        old_retorno = self.tipo_retorno_atual
        self.tipo_retorno_atual = 'void'
        
        self.parse_bloco()
        self.eat('PONTO_VIRG')
        
        self.tabela.sair_escopo()
        self.tipo_retorno_atual = old_retorno

    def parse_decl_funcao(self):
        self.eat('FUNCAO')
        nome = self.current_token.value
        self.eat('ID')
        self.eat('ABRE_PAR')
        params = self.parse_lista_params()
        self.eat('FECHA_PAR')
        self.eat('DOIS_PONTOS')
        tipo_retorno = self.parse_tipo()
        
        # SEMÂNTICO: Registra a função
        tipos_params = [p['tipo'] for p in params]
        self.declarar_simbolo(nome, 'funcao', tipo_retorno, tipos_params)
        
        self.tabela.entrar_escopo()
        for p in params:
            self.declarar_simbolo(p['nome'], 'variavel', p['tipo'])
            
        old_retorno = self.tipo_retorno_atual
        self.tipo_retorno_atual = tipo_retorno
        
        self.parse_bloco()
        self.eat('PONTO_VIRG')
        
        self.tabela.sair_escopo()
        self.tipo_retorno_atual = old_retorno

    def parse_lista_params(self):
        params = []
        if self.current_token.type == 'ID':
            params.append(self.parse_param())
            while self.current_token.type == 'ID':
                params.append(self.parse_param())
        return params

    def parse_param(self):
        nome = self.current_token.value
        self.eat('ID')
        tipo = self.parse_tipo()
        return {'nome': nome, 'tipo': tipo}

    def parse_corpo(self):
        self.eat('INICIO')
        while self.current_token.type != 'FIM':
            self.parse_comando()
            self.eat('PONTO_VIRG')
        self.eat('FIM')

    def parse_comando(self):
        tok = self.current_token.type
        if tok == 'INICIO':
            self.tabela.entrar_escopo()
            self.parse_corpo()
            self.tabela.sair_escopo()
        elif tok == 'SE':
            self.parse_se()
        elif tok == 'ENQUANTO':
            self.parse_enquanto()
        elif tok == 'RETORNE':
            self.parse_retorne()
        elif tok == 'BREAK':
            self.eat('BREAK')
        elif tok == 'CONTINUE':
            self.eat('CONTINUE')
        elif tok == 'ESCREVA':
            self.parse_escreva()
        elif tok == 'ID':
            proximo = self.peek()
            if proximo and proximo.type == 'DOIS_PONTOS':
                self.parse_atribuicao()
            elif proximo and proximo.type == 'ABRE_PAR':
                self.parse_chamada_subrotina()
            else:
                self.error("Esperado ':' ou '(' após ID")
        else:
            self.error("Comando inválido")

    def parse_atribuicao(self):
        nome = self.current_token.value
        self.eat('ID')
        self.eat('DOIS_PONTOS')
        
        simbolo = self.buscar_simbolo(nome)
        if simbolo.categoria != 'variavel':
            self.semantic_error(f"'{nome}' não é uma variável atribuível.")
            
        tipo_expr = self.parse_expressao()
        
        # SEMÂNTICO: Checagem de Tipo Forte
        if simbolo.tipo != tipo_expr:
            self.semantic_error(f"Atribuição inválida. Variável '{nome}' é '{simbolo.tipo}', mas recebeu '{tipo_expr}'.")

    def parse_chamada_subrotina(self):
        nome = self.current_token.value
        self.eat('ID')
        
        simbolo = self.buscar_simbolo(nome)
        if simbolo.categoria != 'funcao':
            self.semantic_error(f"'{nome}' não é uma função/procedimento.")
            
        self.eat('ABRE_PAR')
        args_tipos = self.parse_lista_exp()
        self.eat('FECHA_PAR')
        
        # SEMÂNTICO: Valida quantidade e tipos dos argumentos
        if len(args_tipos) != len(simbolo.params):
            self.semantic_error(f"Função '{nome}' espera {len(simbolo.params)} argumentos, mas recebeu {len(args_tipos)}.")
            
        for i, (tipo_arg, tipo_param) in enumerate(zip(args_tipos, simbolo.params)):
            if tipo_arg != tipo_param:
                self.semantic_error(f"Argumento {i+1} da função '{nome}' deveria ser '{tipo_param}', mas é '{tipo_arg}'.")
                
        return simbolo.tipo # Retorna o tipo da função para a expressão

    def parse_se(self):
        self.eat('SE')
        self.eat('ABRE_PAR')
        tipo_expr = self.parse_expressao()
        if tipo_expr != 'booleano':
            self.semantic_error("A condição do 'se' deve ser uma expressão booleana.")
        self.eat('FECHA_PAR')
        self.eat('ENTAO')
        self.parse_comando()
        if self.current_token.type == 'SENAO':
            self.eat('SENAO')
            self.parse_comando()

    def parse_enquanto(self):
        self.eat('ENQUANTO')
        self.eat('ABRE_PAR')
        tipo_expr = self.parse_expressao()
        if tipo_expr != 'booleano':
            self.semantic_error("A condição do 'enquanto' deve ser booleana.")
        self.eat('FECHA_PAR')
        self.eat('FACA')
        self.parse_comando()

    def parse_retorne(self):
        self.eat('RETORNE')
        tipo_expr = 'void'
        
        if self.current_token.type in ['ID', 'NUMERO', 'LITERAL_CHAR', 'NAO', 'ABRE_PAR', 'VERDADEIRO', 'FALSO', 'MAIS', 'MENOS']:
            tipo_expr = self.parse_expressao()
            
        if self.tipo_retorno_atual != tipo_expr:
            self.semantic_error(f"Função deve retornar '{self.tipo_retorno_atual}', mas tentou retornar '{tipo_expr}'.")

    def parse_escreva(self):
        self.eat('ESCREVA')
        self.eat('ABRE_PAR')
        self.parse_expressao() 
        self.eat('FECHA_PAR')

    def parse_lista_exp(self):
        tipos = []
        if self.current_token.type != 'FECHA_PAR':
            tipos.append(self.parse_expressao())
            while self.current_token.type == 'VIRGULA':
                self.eat('VIRGULA')
                tipos.append(self.parse_expressao())
        return tipos

    def parse_expressao(self):
        tipo_esq = self.parse_expr_simples()
        if self.current_token.type in ['IGUAL', 'DIFERENTE', 'MAIOR', 'MENOR', 'MAIOR_IGUAL', 'MENOR_IGUAL']:
            op = self.current_token.value
            self.eat(self.current_token.type)
            tipo_dir = self.parse_expr_simples()
            
            if tipo_esq != tipo_dir:
                self.semantic_error(f"Não é possível comparar tipos incompativeis ('{tipo_esq}' {op} '{tipo_dir}').")
            return 'booleano' 
            
        return tipo_esq

    def parse_expr_simples(self):
        if self.current_token.type in ['MAIS', 'MENOS', 'NAO']:
            op_unario = self.current_token.type
            self.eat(op_unario)
            
        tipo_esq = self.parse_termo()
        
        while self.current_token.type in ['MAIS', 'MENOS', 'OU']:
            op = self.current_token.type
            self.eat(op)
            tipo_dir = self.parse_termo()
            
            if op in ['MAIS', 'MENOS']:
                if tipo_esq != 'inteiro' or tipo_dir != 'inteiro':
                    self.semantic_error("Operadores '+' e '-' exigem operandos do tipo 'inteiro'.")
                tipo_esq = 'inteiro'
            elif op == 'OU':
                if tipo_esq != 'booleano' or tipo_dir != 'booleano':
                    self.semantic_error("Operador 'ou' exige operandos do tipo 'booleano'.")
                tipo_esq = 'booleano'
                
        return tipo_esq

    def parse_termo(self):
        tipo_esq = self.parse_fator()
        
        while self.current_token.type in ['VEZES', 'DIVIDIDO', 'E']:
            op = self.current_token.type
            self.eat(op)
            tipo_dir = self.parse_fator()
            
            if op in ['VEZES', 'DIVIDIDO']:
                if tipo_esq != 'inteiro' or tipo_dir != 'inteiro':
                    self.semantic_error("Operadores '*' e '/' exigem operandos numéricos.")
                tipo_esq = 'inteiro'
            elif op == 'E':
                if tipo_esq != 'booleano' or tipo_dir != 'booleano':
                    self.semantic_error("Operador 'e' exige operandos booleanos.")
                tipo_esq = 'booleano'
                
        return tipo_esq

    def parse_fator(self):
        tok = self.current_token.type
        if tok == 'ID':
            if self.peek() and self.peek().type == 'ABRE_PAR':
                return self.parse_chamada_subrotina() 
            else:
                simbolo = self.buscar_simbolo(self.current_token.value)
                self.eat('ID')
                return simbolo.tipo 
        elif tok == 'NUMERO':
            self.eat('NUMERO')
            return 'inteiro'
        elif tok == 'LITERAL_CHAR':
            self.eat('LITERAL_CHAR')
            return 'char'
        elif tok == 'VERDADEIRO':
            self.eat('VERDADEIRO')
            return 'booleano'
        elif tok == 'FALSO':
            self.eat('FALSO')
            return 'booleano'
        elif tok == 'ABRE_PAR':
            self.eat('ABRE_PAR')
            tipo = self.parse_expressao()
            self.eat('FECHA_PAR')
            return tipo
        else:
            self.error("Fator inválido")