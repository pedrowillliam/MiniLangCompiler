class ParserTopDown:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def error(self, msg):
        raise SyntaxError(f"Erro Sintático na linha {self.current_token.line}: {msg}. Encontrado: '{self.current_token.value}' ({self.current_token.type})")

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

    # --- Regras da Gramática ---
    def parse_programa(self):
        print(f"-> Iniciando análise do Programa...")
        self.eat('PROGRAMA')
        self.eat('ID')
        self.parse_bloco()
        if self.current_token.type != 'EOF':
            self.error("Código extra encontrado após o fim do programa")
        print("<- Análise concluída com sucesso!")

    def parse_bloco(self):
        while self.current_token.type == 'VAR':
            self.parse_decl_var()
        while self.current_token.type in ('PROCEDIMENTO', 'FUNCAO'):
            self.parse_decl_subrotina()
        self.parse_corpo()

    def parse_decl_var(self):
        self.eat('VAR')
        self.parse_lista_ids()
        self.parse_tipo()
        self.eat('PONTO_VIRG')

    def parse_lista_ids(self):
        self.eat('ID')
        while self.current_token.type == 'ID':
            self.eat('ID')

    def parse_tipo(self):
        if self.current_token.type in ['INTEIRO', 'BOOLEANO']:
            self.eat(self.current_token.type)
        else:
            self.error("Esperado tipo (inteiro ou booleano)")

    def parse_decl_subrotina(self):
        if self.current_token.type == 'PROCEDIMENTO':
            self.parse_decl_procedimento()
        elif self.current_token.type == 'FUNCAO':
            self.parse_decl_funcao()

    def parse_decl_procedimento(self):
        self.eat('PROCEDIMENTO')
        self.eat('ID')
        self.eat('ABRE_PAR')
        self.parse_lista_params()
        self.eat('FECHA_PAR')
        self.parse_bloco()
        self.eat('PONTO_VIRG')

    def parse_decl_funcao(self):
        self.eat('FUNCAO')
        self.eat('ID')
        self.eat('ABRE_PAR')
        self.parse_lista_params()
        self.eat('FECHA_PAR')
        self.eat('DOIS_PONTOS')
        self.parse_tipo()
        self.parse_bloco()
        self.eat('PONTO_VIRG')

    def parse_lista_params(self):
        if self.current_token.type == 'ID':
            self.parse_param()
            while self.current_token.type == 'ID':
                self.parse_param()

    def parse_param(self):
        self.eat('ID')
        self.parse_tipo()

    def parse_corpo(self):
        self.eat('INICIO')
        while self.current_token.type != 'FIM':
            self.parse_comando()
            self.eat('PONTO_VIRG')
        self.eat('FIM')

    def parse_comando(self):
        tok = self.current_token.type
        if tok == 'INICIO':
            self.parse_corpo()
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
            # Lookahead para decidir
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
        self.eat('ID')
        self.eat('DOIS_PONTOS')
        self.parse_expressao()

    def parse_chamada_subrotina(self):
        self.eat('ID')
        self.eat('ABRE_PAR')
        self.parse_lista_exp()
        self.eat('FECHA_PAR')

    def parse_se(self):
        self.eat('SE')
        self.eat('ABRE_PAR')
        self.parse_expressao()
        self.eat('FECHA_PAR')
        self.eat('ENTAO')
        self.parse_comando()
        if self.current_token.type == 'SENAO':
            self.eat('SENAO')
            self.parse_comando()

    def parse_enquanto(self):
        self.eat('ENQUANTO')
        self.eat('ABRE_PAR')
        self.parse_expressao()
        self.eat('FECHA_PAR')
        self.eat('FACA')
        self.parse_comando()

    def parse_retorne(self):
        self.eat('RETORNE')
        if self.current_token.type in ['ID', 'NUMERO', 'NAO', 'ABRE_PAR', 'VERDADEIRO', 'FALSO', 'MAIS', 'MENOS']:
            self.parse_expressao()

    def parse_escreva(self):
        self.eat('ESCREVA')
        self.eat('ABRE_PAR')
        self.parse_expressao()
        self.eat('FECHA_PAR')

    def parse_lista_exp(self):
        if self.current_token.type != 'FECHA_PAR':
            self.parse_expressao()
            while self.current_token.type == 'VIRGULA':
                self.eat('VIRGULA')
                self.parse_expressao()

    def parse_expressao(self):
        self.parse_expr_simples()
        if self.current_token.type in ['IGUAL', 'DIFERENTE', 'MAIOR', 'MENOR', 'MAIOR_IGUAL', 'MENOR_IGUAL']:
            self.eat(self.current_token.type)
            self.parse_expr_simples()

    def parse_expr_simples(self):
        if self.current_token.type in ['MAIS', 'MENOS', 'NAO']:
            self.eat(self.current_token.type)
        self.parse_termo()
        while self.current_token.type in ['MAIS', 'MENOS', 'OU']:
            self.eat(self.current_token.type)
            self.parse_termo()

    def parse_termo(self):
        self.parse_fator()
        while self.current_token.type in ['VEZES', 'DIVIDIDO', 'E']:
            self.eat(self.current_token.type)
            self.parse_fator()

    def parse_fator(self):
        tok = self.current_token.type
        if tok == 'ID':
            if self.peek() and self.peek().type == 'ABRE_PAR':
                self.parse_chamada_subrotina()
            else:
                self.eat('ID')
        elif tok == 'NUMERO':
            self.eat('NUMERO')
        elif tok == 'VERDADEIRO':
            self.eat('VERDADEIRO')
        elif tok == 'FALSO':
            self.eat('FALSO')
        elif tok == 'ABRE_PAR':
            self.eat('ABRE_PAR')
            self.parse_expressao()
            self.eat('FECHA_PAR')
        else:
            self.error("Fator inválido")