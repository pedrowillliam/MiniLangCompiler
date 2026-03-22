import sys
import os

try:
    from src.lexer import Lexer
    from src.parser import ParserTopDown
    from src.ast_printer import ASTPrinter
    from src.semantic import AnalisadorSemantico
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Verifique se a pasta 'src' existe e contém 'lexer.py' e 'parser.py'.")
    sys.exit(1)

def carregar_arquivo(caminho):
    try:
        if not os.path.exists(caminho):
            raise FileNotFoundError
        with open(caminho, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo '{caminho}' não foi encontrado.")
        print("Dica: Verifique se a pasta 'testes' existe e se o nome do arquivo está correto.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        sys.exit(1)

def main():
    print("==========================================")
    print("   MINILANG COMPILER - UFAPE       ")
    print("==========================================")
    
    # Caso teste:
    arquivo_padrao = 'tests/program_test_float.txt'
    
    if len(sys.argv) > 1:
        arquivo_teste = sys.argv[1]
    else:
        arquivo_teste = arquivo_padrao

    print(f"📂 Arquivo selecionado: {arquivo_teste}")
    codigo_fonte = carregar_arquivo(arquivo_teste)

    try:
        print("\n[1/4] Iniciando Análise Léxica...")
        lexer = Lexer(codigo_fonte)
        print(f"   ✓ Sucesso! {len(lexer.tokens)} tokens gerados.")

        print("\n--- LISTA DE TOKENS GERADOS (LEXER) ---")
        for token in lexer.tokens:
            print(f"  {token}")
        print("---------------------------------------")

        print("\n[2/4] Iniciando Análise Sintática (Gerando AST)...")
        parser = ParserTopDown(lexer.tokens)
        
        arvore = parser.parse_programa() 
        
        print("\n[3/4] Imprimindo a Árvore Sintática Abstrata (AST):")
        print("--------------------------------------------------")
        
        impressor = ASTPrinter()
        impressor.imprimir(arvore)

        print("\n[4/4] Iniciando Análise Semântica...")
        semantico = AnalisadorSemantico()
        semantico.analisar(arvore) 
        print("   ✓ Sucesso! Tipagem e declarações validadas.")
        
        print("--------------------------------------------------")
        print("\n✅ COMPILAÇÃO CONCLUÍDA: O programa é sintática e semanticamente válido!")

    except SyntaxError as e:
        print(f"\n❌ ERRO SINTÁTICO DETECTADO:")
        print(f"   {e}")
    except Exception as e:
        if "Erro Semântico" in str(e):
            print(f"\n❌ ERRO SEMÂNTICO DETECTADO:")
            print(f"   {e}")
        else:
            print(f"\n❌ ERRO INTERNO (BUG): {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()