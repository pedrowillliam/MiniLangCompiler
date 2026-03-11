class Simbolo:
    def __init__(self, nome, categoria, tipo, params=None):
        self.nome = nome
        self.categoria = categoria  # Pode ser 'variavel' ou 'funcao'
        self.tipo = tipo            # 'inteiro', 'booleano', 'char', 'void'
        self.params = params or []  # Se for função, guarda a lista de tipos esperados

    def __repr__(self):
        return f"Simbolo(nome='{self.nome}', cat='{self.categoria}', tipo='{self.tipo}', params={self.params})"

class TabelaSimbolos:
    def __init__(self):
        # A pilha começa com um dicionário vazio (Escopo Global)
        self.pilha_escopos = [{}]

    def entrar_escopo(self):
        """Empurra um novo dicionário vazio para a pilha."""
        self.pilha_escopos.append({})
        # print("DEBUG: Novo escopo criado.") 

    def sair_escopo(self):
        """Remove o escopo atual (topo da pilha)."""
        if len(self.pilha_escopos) > 1:
            self.pilha_escopos.pop()
            # print("DEBUG: Escopo destruído.")
        else:
            raise Exception("Erro Interno: Tentativa de destruir o escopo global.")

    def declarar(self, nome, categoria, tipo, params=None):
        """Declara um símbolo no escopo atual."""
        escopo_atual = self.pilha_escopos[-1]
        
        # Verifica se já existe UMA variável/função com este nome NESTE MESMO escopo
        if nome in escopo_atual:
            raise Exception(f"Erro Semântico: O identificador '{nome}' já foi declarado neste escopo.")
        
        # Salva o símbolo no dicionário atual
        escopo_atual[nome] = Simbolo(nome, categoria, tipo, params)

    def buscar(self, nome):
        """
        Busca um símbolo começando do escopo mais interno (topo da pilha)
        indo até o escopo global (base da pilha).
        """
        for escopo in reversed(self.pilha_escopos):
            if nome in escopo:
                return escopo[nome]
        
        # Retorna None se não encontrar em nenhum escopo
        return None