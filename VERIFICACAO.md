# Verificação do MiniLangCompiler contra as Anotações

## Anotação 1: Tabela de símbolos gerada na parte sintática ou semântica
✅ **CORRETO**: A tabela de símbolos é criada APENAS na análise semântica (em `semantic.py`)
- Criada em: `AnalisadorSemantico.__init__()` 
- Usada após AST estar completamente preenchida

## Anotação 2: Tabela de simbolismo usa extremamente a parte LÉXICA
✅ **CORRETO**: A tabela usa informações do léxico através dos tokens:
- Cada nó da AST armazena o `token` léxico original
- Em `semantic_error()`, extrai linha do token: `node.token.line`
- Identificadores usam: `node.name` (do token)

## Anotação 3: Lista de tokens incoerente
✅ **COERENTE**: Lista de tokens está bem estruturada
- Mostra: tipo, valor, linha do token
- Exemplo: `Token(NUMERO, '10', linha 18)`
- Tokens filtram comentários e espaços em branco corretamente

## Anotação 4: Análise semântica varrendo código ou lista de tokens
✅ **CORRETO**: A análise semântica varre a AST, NÃO lista de tokens
- Implementa padrão Visitor: `analisar(node)` → `visit_TipoNode(node)`
- Percorre AST: ProgramNode → BlockNode → Comandos
- Não processa tokens diretamente

## Anotação 5: Confusão com tipos de erros
✅ **CORRETO**: Tipos de erros bem identificados
- Erro Léxico: caractere ilegal (em `lexer.py`)
- Erro Sintático: token inesperado (em `parser.py`)
- Erro Semântico: tipos, declarações, escopos (em `semantic.py`)

## Anotação 6: Tabela criada e usada APÓS AST preenchida
✅ **CORRETO**: Fluxo exato esperado
1. main.py: Lexer → Parser (AST gerada)
2. main.py: Imprime AST
3. main.py: AnalisadorSemantico.analisar(arvore) - APÓS AST pronta

## Problemas Identificados e Correções Necessárias

### ✅ Melhorias Estruturais Implementadas:

#### 1. **Escopo para blocos IF/WHILE** - ✅ IMPLEMENTADO
   - **Status**: CONCLUÍDO
   - **Localização**: `visit_IfNode()` (linhas 148-175) e `visit_WhileNode()` (linhas 177-191)
   - **Implementação**:
     ```python
     # visit_IfNode:
     if isinstance(node.true_block, BlockNode) and len(node.true_block.vars_decl) > 0:
         self.tabela.entrar_escopo()
         self.analisar(node.true_block)
         self.tabela.sair_escopo()
     else:
         self.analisar(node.true_block)
     ```
   - **O que mudou**: Agora cria um novo escopo quando há variáveis dentro de blocos IF/WHILE
   - **Impacto Lógico**: ✅ Variáveis declaradas em blocos internos não causam conflito com escopo externo

#### 2. **Retornos explícitos em todos os méthods visit** - ✅ IMPLEMENTADO
   - **Status**: CONCLUÍDO
   - **Métodos corrigidos**:
     | Método | Antes | Depois | Linha |
     |--------|-------|--------|-------|
     | `visit_ProgramNode` | Sem return | `return None` | 31 |
     | `visit_BlockNode` | Sem return | `return None` | 48 |
     | `visit_VarDeclNode` | Sem return | `return None` | 59 |
     | `visit_AssignNode` | Sem return | `return None` | 82 |
     | `visit_IfNode` | Sem return | `return None` | 175 |
     | `visit_WhileNode` | Sem return | `return None` | 191 |
     | `visit_SubroutineNode` | Sem return | `return None` | 213 |
     | `visit_ReturnNode` | Sem return | `return None` | 220 |
     | `visit_PrintNode` | Sem return | `return None` | 247 |
     | `visit_BreakNode` | `pass` | `return None` | 250 |
     | `visit_ContinueNode` | `pass` | `return None` | 252 |
   - **Impacto Lógico**: ✅ Nenhuma mudança no comportamento (retorno implícito já era `None`)
   - **Benefício**: Explicitação deixa código mais claro e evita warnings do Pylance

#### 3. **Validação de tipos de argumentos** - ✅ FUNCIONANDO CORRETAMENTE
   - **Status**: NÃO NECESSITAVA CORREÇÃO (já estava correto)
   - **Localização**: `visit_FunctionCallNode()` (linhas 232-239)
   - **Implementação**:
     ```python
     for i, (tipo_arg, tipo_param) in enumerate(zip(args_analisados, simbolo.params)):
         if tipo_arg != tipo_param:
             self.semantic_error(node.id_node, f"Argumento {i+1} de '{nome}' deve ser '{tipo_param}', mas é '{tipo_arg}'.")
     ```
   - **Impacto Lógico**: ✓ Funciona corretamente comparando strings ('inteiro', 'char', etc.)

### Resumo:
- ✅ Arquitetura correta: LÉXICO → SINTÁTICO → SEMÂNTICO
- ✅ Fluxo de tabela de símbolos correto
- ✅ Tratamento de erros bem dividido
- ✅ Escopo para blocos IF/WHILE implementado
- ✅ Retornos explícitos em todos os methods visit
- ✅ Validação de tipos de argumentos funcionando corretamente

### Status Final do Código:
O projeto agora está **robusto, completo e segue as anotações especificadas**.
Todas as melhorias foram implementadas para melhorar:
1. **Clareza** - Retornos explícitos deixam intenção clara
2. **Robustez** - Escopos bem definidos evitam conflitos de variáveis
3. **Manutenibilidade** - Código mais limpo e fácil de entender
