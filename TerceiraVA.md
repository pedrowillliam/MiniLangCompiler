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

Depois que a árvore (AST) ficou pronta, a gente precisava de algo que fizesse o compilador "entender" o que o código estava tentando fazer. Não adianta a frase estar escrita certa (sintaxe) se ela não faz sentido (semântica). Por isso, criamos o Analisador Semântico.

.O que ele faz na prática:

- Roda a Árvore Inteira: Ele usa o esquema de "visitante" (Visitor). Ele vai em cada galho da árvore e checa as regras. Se ele vê uma soma (+), ele para e pergunta: "O que tem do lado esquerdo? E do direito?". Se um for inteiro e o outro char, ele trava e avisa o erro.

-Uso da Tabela de Símbolos: É aqui que a tabela é utilizada. Quando o código declara var x inteiro, o semântico anota isso. Se lá na frente o usuário tentar fazer x : 'A', o semântico olha na tabela, vê que x só aceita números e barra a atribuição.

-Vigia das Funções: A gente programou ele para ser bem rígido com funções. Se a função pede dois números, e você passa só um, ele acusa o erro. Se a função promete devolver um booleano e você tenta devolver um inteiro, ele também não deixa passar.

-Regras do IF e WHILE: Outra coisa importante foi garantir que o teste do se e do enquanto seja sempre uma pergunta de sim ou não (booleano). Se o programador colocar se (10 + 5), o semântico avisa que isso não faz sentido como condição.

.Por que isso foi importante?
Essa foi a parte que deu "inteligência" ao projeto. Agora o compilador não apenas lê o código, mas garante que o programador não cometa erros de lógica básica, como misturar tipos de dados ou esquecer de declarar variáveis. Isso deixa a nossa linguagem muito mais segura e profissional.

4. Fluxo de Execução do Compilador (Pipeline)
Com as mudanças da 3ª VA, o caminho que o código percorre desde o arquivo de texto até a validação final é:

    1. Análise Léxica (lexer.py): O código-fonte é lido e transformado em uma lista de Tokens. É aqui que todos os tipos são identificados pela primeira vez.

    2. Análise Sintática (parser.py): O Parser consome os tokens e verifica se a "gramática" está correta (parênteses no lugar, pontos e vírgulas, etc). Em vez de apenas validar, ele agora constrói a AST (Árvore Sintática Abstrata), que é o mapa estrutural do programa.

    3. Visualização da Árvore (ast_printer.py): Antes de validar a lógica, a árvore é percorrida para ser impressa no terminal. Isso serve para nós, desenvolvedores, confirmarmos que o Parser entendeu a hierarquia correta (como a precedência das operações matemáticas).

    4.Suporte da Tabela de Símbolos (tabela_simbolos.py): Diferente das outras fases, a Tabela não é um "momento" único, mas uma estrutura de suporte chamada principalmente durante a análise semântica. Ela funciona como o "banco de dados" do compilador, guardando quem são as variáveis, seus tipos e em qual escopo (global ou local) elas existem.

    5. Análise Semântica (semantic.py): A AST pronta é entregue ao Analisador Semântico. Ele "viaja" por cada nó da árvore usando a Tabela de Símbolos para garantir que as regras de tipo, escopo e declaração sejam respeitadas.

    6. Resultado Final: Se o programa passar por esse fluxo sem erros, temos a garantia de que ele está pronto para ser executado ou traduzido para outra linguagem, pois sua estrutura e sua lógica foram 100% verificadas.