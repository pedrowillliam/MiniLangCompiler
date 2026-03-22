Lista de mudanças para a terceira VA:

1. IMPLEMENTACAO DO TIPO FLOAT :

.Alterações Lexicas (Lexer):

-Palavra Reservada: FLOAT (float), permitindo a declaracao de variaveis e retornos de funcoes com este tipo.
-Literal Numerico: NUMERO_FLOAT (ex: 3.14), para identificar valores decimais.

posicionado a regra do NUMERO_FLOAT antes da regra do NUMERO inteiro. Para evitar problema do lexer ser "guloso" e fatiar um numero como 3.14 em tres partes (3, ., 14), garantindo que o valor decimal seja lido como um token unico e coeso.

.Alterações Sintaticas (Parser):

-A regra de tipos agora aceita a palavra reservada float.
-A regra de fatores matematicos agora aceita o terminal numero_float, permitindo que decimais sejam usados dentro de expressoes.

.testes:

-inteiro operando com inteiro = Valido (retorna inteiro)
-float operando com float = Valido (retorna float)
-inteiro operando com float = ERRO SEMANTICO (Incompatibilidade de tipos)

2. Implementação da ÁRVORE SINTATICA ABSTRATA (AST):

Nesta etapa, o compilador sofreu sua maior refatoracao estrutural, abandonando esse modelo "Single-Pass" (onde a analise sintatica e semantica ocorrem simultaneamente) para adotar uma arquitetura "Multi-Pass".

.Mudancas Arquiteturais e Novos Modulos:

-Criacao do modulo ast_node.py: Foram implementadas as classes que representam os nos da Arvore Sintatica Abstrata. A estrutura foi dividida hierarquicamente em Nos de Valores Basicos (NumeroIntNode, IdentifierNode), Nos de Expressoes (BinOpNode, UnaryOpNode) e Nos de Comandos/Fluxo (AssignNode, IfNode, BlockNode, ProgramNode).

.Refatoracao do Analisador Sintatico (parser.py):

-Remocao da Semantica: A Tabela de Simbolos e todas as checagens de tipos e declaracoes foram completamente removidas do Parser.

-Responsabilidade Unica: O Parser agora atua estritamente na validacao da gramatica (sintaxe). Ao ler uma expressao, em vez de tentar resolve-la ou buscar variaveis, ele apenas instancia os respectivos nos da AST e os conecta.

-Retorno: Ao final da execucao, o Parser devolve a raiz da arvore (ProgramNode), que contem toda a estrutura do codigo-fonte mapeada em memoria.

.Implementacao do AST Printer (ast_printer.py):
Criamos uma classe utilitaria baseada no padrao de projeto "Visitor Pattern". O objetivo desta classe e percorrer a arvore gerada pelo Parser e imprimi-la no terminal de forma identada e visual. Isso permitiu validar se a precedencia matematica e o aninhamento de blocos (como If e While) estao sendo construidos corretamente pelo Parser antes de enviarmos a arvore para a analise semantica.

.Justificativa do Projeto:
Separar a arvore (sintaxe) das regras de negocio (semantica) torna o compilador extremamente modular, facilitando a deteccao de bugs e preparando o terreno para futuras otimizacoes de codigo e para a fase de geracao de codigo alvo.


