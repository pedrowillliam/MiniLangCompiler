Lista de mudanças para a terceira VA:

1. IMPLEMENTACAO DO TIPO FLOAT :

Alterações Lexicas (Lexer):

-Palavra Reservada: FLOAT (float), permitindo a declaracao de variaveis e retornos de funcoes com este tipo.
-Literal Numerico: NUMERO_FLOAT (ex: 3.14), para identificar valores decimais.

posicionado a regra do NUMERO_FLOAT antes da regra do NUMERO inteiro. Para evitar problema do lexer ser "guloso" e fatiar um numero como 3.14 em tres partes (3, ., 14), garantindo que o valor decimal seja lido como um token unico e coeso.

Alterações Sintaticas (Parser):

-A regra de tipos agora aceita a palavra reservada float.
-A regra de fatores matematicos agora aceita o terminal numero_float, permitindo que decimais sejam usados dentro de expressoes.

testes:

-inteiro operando com inteiro = Valido (retorna inteiro)
-float operando com float = Valido (retorna float)
-inteiro operando com float = ERRO SEMANTICO (Incompatibilidade de tipos)

2. 
