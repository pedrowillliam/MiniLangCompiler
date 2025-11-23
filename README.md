# MiniLang Compiler: Analisador Léxico e Sintático Top-Down

## 📄 Sobre o Projeto
Este projeto consiste na implementação das fases iniciais de um compilador (Front-end) para a linguagem procedural didática **MiniLang**. Desenvolvido em **Python**, o sistema é composto por um **Analisador Léxico (Scanner)** e um **Analisador Sintático (Parser)**.

O objetivo principal é demonstrar a aplicação prática de conceitos da teoria de compiladores, especificamente focando na estruturação de gramáticas **LL(1)** e na implementação de um **Parser de Descida Recursiva (Recursive Descent)**.

## 🚀 Funcionalidades

### 1. Análise Léxica (Tokenização)
* Processamento do código fonte via Expressões Regulares (`regex`).
* Identificação e classificação de tokens (palavras reservadas, identificadores, literais numéricos, operadores e delimitadores).
* Remoção automática de espaços em branco e comentários aninhados entre chaves `{ ... }`.
* Relatório de erros léxicos com indicação de linha.

### 2. Análise Sintática (Parsing)
* **Abordagem Top-Down:** Implementação via Descida Recursiva, onde cada regra da gramática BNF é mapeada diretamente para uma função Python.
* **Tratamento LL(1):** Utilização de *Lookahead* (espiar o próximo token) para resolver conflitos de derivação, especificamente na distinção entre comandos de Atribuição (`x : 1`) e Chamada de Procedimento (`soma(x y)`).
* Validação estrutural de blocos, declarações de variáveis, subrotinas (funções e procedimentos) e estruturas de controle (`se/senao`, `enquanto`).
* Sistema de tratamento de erros sintáticos que aponta a linha exata e o token inesperado.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Bibliotecas:** `re`, `sys`, `os`.
* **Paradigma:** Orientação a Objetos (modularização em classes `Lexer` e `ParserTopDown`).

## 📋 Estrutura da Linguagem (MiniLang)
O compilador reconhece uma linguagem estruturada similar a Pascal, com as seguintes características:
* **Tipos:** `inteiro`, `booleano`.
* **Estrutura:** Programa principal, declaração de variáveis globais e subrotinas.
* **Controle de Fluxo:** `se...entao...senao`, `enquanto...faca`.
* **Subrotinas:** `procedimento` (sem retorno) e `funcao` (com retorno).
* **Comandos Especiais:** `break`, `continue`, `retorne`, `escreva`.

## 📂 Estrutura de Arquivos
O projeto está organizado de forma modular:

```text
MiniLangCompiler/
├── src/
│   ├── lexer.py      # Lógica de tokenização e definições de regex
│   └── parser.py     # Implementação da gramática via Descida Recursiva
├── testes/
│   ├── programa_sucesso.txt  # Casos de teste válidos
│   └── programa_erro.txt     # Casos de teste para validação de erros
└── main.py           # Ponto de entrada (Driver code)
