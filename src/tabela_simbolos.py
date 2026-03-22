class Simbolo:
    def __init__(self, nome, categoria, tipo, params=None):
        self.nome = nome
        self.categoria = categoria  
        self.tipo = tipo            
        self.params = params or []  

    def __repr__(self):
        return f"Simbolo(nome='{self.nome}', cat='{self.categoria}', tipo='{self.tipo}', params={self.params})"

class TabelaSimbolos:
    def __init__(self):
        self.pilha_escopos = [{}]

    def entrar_escopo(self):
        """Empurra um novo dicionário vazio para a pilha."""
        self.pilha_escopos.append({}) 

    def sair_escopo(self):
        """Remove o escopo atual (topo da pilha)."""
        if len(self.pilha_escopos) > 1:
            self.pilha_escopos.pop()
        else:
            raise Exception("Erro Interno: Tentativa de destruir o escopo global.")

    def declarar(self, nome, categoria, tipo, params=None):
        """Declara um símbolo no escopo atual."""
        escopo_atual = self.pilha_escopos[-1]
        
        if nome in escopo_atual:
            raise Exception(f"Erro Semântico: O identificador '{nome}' já foi declarado neste escopo.")
        
        escopo_atual[nome] = Simbolo(nome, categoria, tipo, params)

    def buscar(self, nome):
        """
        Busca um símbolo começando do escopo mais interno (topo da pilha)
        indo até o escopo global (base da pilha).
        """
        for escopo in reversed(self.pilha_escopos):
            if nome in escopo:
                return escopo[nome]
        
        return None