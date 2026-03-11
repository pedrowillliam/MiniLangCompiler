# Gramática MiniLang - Fase 2 (Análise Semântica)

Esta é a gramática em notação BNF (Backus-Naur Form) atualizada para a Fase 2 do compilador MiniLang. A linguagem foi projetada para ser **LL(1)** (sem recursão à esquerda e fatorada para análise *top-down* com 1 token de *lookahead*).

## Atualizações da Fase 2:
* **Sistema de Tipos:** Adição dos tipos `char` e `void`.
* **Tipagem Forte e Estática:** Regras de validação na Tabela de Símbolos.
* **Literais:** Suporte a caracteres literais entre aspas simples (ex: `'a'`).

---

## 1. Estrutura Principal
```bnf
<programa> ::= programa <identificador>; <bloco>
<bloco> ::= { <decl_var> } { <decl_subrotina> } <corpo>
<corpo> ::= inicio { <comando>; } fim

<decl_var> ::= var <lista_ids> <tipo>;
<lista_ids> ::= <identificador> { <identificador> }

--declarações e tipos

<tipo> ::= inteiro | booleano | char | void

<decl_subrotina> ::= <decl_funcao> | <decl_procedimento>
<decl_procedimento> ::= procedimento <identificador> ( [ <lista_params> ] ) <bloco>;
<decl_funcao> ::= funcao <identificador> ( [ <lista_params> ] ): <tipo> <bloco>;

<lista_params> ::= <param> { <param> }
<param> ::= <identificador> <tipo>

--comandos

<comando> ::= <comando_composto>
            | <atribuicao>
            | <chamada_subrotina>
            | <se>
            | <enquanto>
            | <retorne>
            | <break_stmt>
            | <continue_stmt>
            | <escreva>

<comando_composto> ::= <corpo>
<atribuicao> ::= <identificador> : <expressao>
<chamada_subrotina> ::= <identificador> ( [ <lista_exp> ] )

<se> ::= se ( <expressao> ) entao <comando> [ senao <comando> ]
<enquanto> ::= enquanto ( <expressao> ) faca <comando>
<retorne> ::= retorne [ <expressao> ]
<break_stmt> ::= break
<continue_stmt> ::= continue
<escreva> ::= escreva ( <expressao> )

<lista_exp> ::= <expressao> { , <expressao> }

--expressões e operadores

<expressao> ::= <expr_simples> [ <op_rel> <expr_simples> ]
<op_rel> ::= == | != | > | >= | < | <=

<expr_simples> ::= [ <sinal_unario> ] <termo> { <add_op> <termo> }
<sinal_unario> ::= + | - | nao
<add_op> ::= + | - | ou

<termo> ::= <fator> { <mul_op> <fator> }
<mul_op> ::= * | / | e

<fator> ::= <identificador>
          | <numero>
          | <literal_char>
          | verdadeiro
          | falso
          | <chamada_subrotina>
          | ( <expressao> )

-- Regras Lexicas Base

<literal_char> ::= ' <caractere> '
<identificador> ::= <letra> { <letra> | <digito> }
<numero> ::= <digito> { <digito> }
<caractere> ::= <letra> | <digito> | <simbolo_qualquer>
<digito> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<letra> ::= a | b | ... | z | A | B | ... | Z
