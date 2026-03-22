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


3. Implementação da semantic.py

Após a construção da AST, foi necessária a implementação de um mecanismo para validar o "sentido" do código. Não basta a sintaxe estar correta se as operações não fizerem sentido lógico. Para isso, criamos o Analisador Semântico.

O que ele faz na prática:

.Varredura da Árvore (Visitor Pattern): O analisador percorre cada nó da árvore validando as regras de negócio da linguagem. Ao encontrar uma operação de soma (+), por exemplo, ele verifica os nós filhos (esquerdo e direito). Se houver incompatibilidade (como somar um inteiro com um char), o processo é interrompido e o erro é reportado.

.Uso e Alimentação da Tabela de Símbolos: É nesta etapa que a tabela brilha. Quando o código declara var x inteiro, o semântico registra o símbolo, sua categoria e seu tipo. Além disso, a tabela utiliza uma pilha de escopos, garantindo que variáveis locais de uma função não interfiram em variáveis globais ou de outras funções. Se o programador tentar atribuir um valor incompatível (x : 'A'), o semântico consulta a tabela e bloqueia a ação.

.Validação Estrita de Funções: O analisador é rigoroso com as assinaturas das funções. Ele garante que a quantidade e o tipo dos argumentos passados na chamada correspondam exatamente aos parâmetros exigidos na declaração. Também valida se o tipo de retorno coincide com o que a função promete devolver.

.Regras de Controle de Fluxo (IF e WHILE): Garantimos que as expressões de teste das estruturas de controle resultem estritamente em um valor booleano. Se o programador escrever algo como se (10 + 5), o semântico acusará que a condição é inválida.

.Por que isso foi importante?
Essa etapa deu "inteligência" ao projeto. Agora o compilador não apenas estrutura o código, mas garante que o programador não cometa erros de lógica fundamentais, como misturar tipos de dados de forma insegura, violar escopos ou esquecer declarações. Isso eleva a robustez e a segurança da nossa linguagem.

4. Fluxo de Execução do Compilador (Pipeline)
Com as mudanças da 3ª VA, o caminho que o código percorre desde o arquivo de texto até a validação final é:

    1.Ponto de Entrada e Orquestração (main.py): Atua como o "maestro" do compilador. Ele é responsável por carregar o arquivo de texto contendo o código-fonte, orquestrar a chamada de cada fase na ordem correta, imprimir os relatórios de execução no terminal (como a lista de tokens e a impressão da AST) e capturar as exceções, exibindo mensagens de erro formatadas e precisas para o usuário.

    2. Análise Léxica (lexer.py): O código-fonte é lido e transformado em uma lista de Tokens. É aqui que todos os tipos são identificados pela primeira vez.

    3. Análise Sintática (parser.py): O Parser consome os tokens e verifica se a "gramática" está correta (parênteses no lugar, pontos e vírgulas, etc). Em vez de apenas validar, ele agora constrói a AST (Árvore Sintática Abstrata), que é o mapa estrutural do programa.

    4. Visualização da Árvore (ast_printer.py): Antes de validar a lógica, a árvore é percorrida para ser impressa no terminal. Isso serve para nós, desenvolvedores, confirmarmos que o Parser entendeu a hierarquia correta (como a precedência das operações matemáticas).

    5.Suporte da Tabela de Símbolos (tabela_simbolos.py): Diferente das outras fases, a Tabela não é um "momento" único, mas uma estrutura de suporte chamada principalmente durante a análise semântica. Ela funciona como o "banco de dados" do compilador, guardando quem são as variáveis, seus tipos e em qual escopo (global ou local) elas existem.

    6. Análise Semântica (semantic.py): A AST pronta é entregue ao Analisador Semântico. Ele "viaja" por cada nó da árvore usando a Tabela de Símbolos para garantir que as regras de tipo, escopo e declaração sejam respeitadas.

    7. Resultado Final: Se o programa passar por esse fluxo sem erros, temos a garantia de que ele está pronto para ser executado ou traduzido para outra linguagem, pois sua estrutura e sua lógica foram 100% verificadas.