import sys
import os

try:
    from src.lexer import Lexer
    from src.parser import ParserTopDown
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
    print("   MINILANG COMPILER - UFAPE (BETA)       ")
    print("==========================================")

    # ---------------------------------------------------------
    # 1. Definição do arquivo de entrada (PADRÃO)
    # ---------------------------------------------------------
    
    # Caso teste:
    arquivo_padrao = 'tests/program_semantic_errors.txt'
    
    # Lógica de Seleção:
    # Se o usuário passou um arquivo no terminal, usa ele. Senão, usa o padrão acima.
    if len(sys.argv) > 1:
        arquivo_teste = sys.argv[1]
    else:
        arquivo_teste = arquivo_padrao

    print(f"📂 Arquivo selecionado: {arquivo_teste}")
    codigo_fonte = carregar_arquivo(arquivo_teste)

    try:
        # -----------------------------------------------------
        # 2. Análise Léxica (Scanner)
        # -----------------------------------------------------
        print("\n[1/2] Iniciando Análise Léxica...")
        lexer = Lexer(codigo_fonte)
        print(f"   ✓ Sucesso! {len(lexer.tokens)} tokens gerados.")

        # -----------------------------------------------------
        # 3. Análise Sintática (Parser Top-Down)
        # -----------------------------------------------------
        print("[2/2] Iniciando Análise Sintática (Top-Down)...")
        parser = ParserTopDown(lexer.tokens)
        parser.parse_programa()
        
        print("\n✅ COMPILAÇÃO CONCLUÍDA: O código é válido segundo a gramática!")

    except SyntaxError as e:
        print(f"\n❌ ERRO SINTÁTICO DETECTADO:")
        print(f"   {e}")
    except Exception as e:
        # Verifica se é um erro semântico que nós mesmos criamos
        if "Erro Semântico" in str(e):
            print(f"\n❌ ERRO SEMÂNTICO DETECTADO:")
            print(f"   {e}")
        else:
            print(f"\n❌ ERRO INTERNO (BUG): {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()