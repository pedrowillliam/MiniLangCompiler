import re

TOKEN_TYPES = [
    ('COMENTARIO', r'\{.*?\}'),
    ('LITERAL_CHAR', r"'[^']'"),
    ('NUMERO_FLOAT', r'\d+\.\d+'),
    ('NUMERO',     r'\d+'),
    ('PROGRAMA',   r'programa\b'),    
    ('VAR',        r'var\b'),          
    ('INTEIRO',    r'inteiro\b'),
    ('FLOAT',      r'float\b'),
    ('BOOLEANO',   r'booleano\b'),
    ('CHAR',         r'char\b'),      
    ('VOID',         r'void\b'),       
    ('PROCEDIMENTO', r'procedimento\b'),
    ('FUNCAO',     r'funcao\b'),
    ('INICIO',     r'inicio\b'),
    ('FIM',        r'fim\b'),
    ('SE',         r'se\b'),           
    ('ENTAO',      r'entao\b'),
    ('SENAO',      r'senao\b'),
    ('ENQUANTO',   r'enquanto\b'),
    ('FACA',       r'faca\b'),
    ('RETORNE',    r'retorne\b'),
    ('ESCREVA',    r'escreva\b'),
    ('BREAK',      r'break\b'),
    ('CONTINUE',   r'continue\b'),
    ('E',          r'e\b'),            
    ('OU',         r'ou\b'),
    ('NAO',        r'nao\b'),
    ('VERDADEIRO', r'verdadeiro\b'),
    ('FALSO',      r'falso\b'),
    ('ID',         r'[a-zA-Z][a-zA-Z0-9]*'), 
    ('IGUAL',      r'=='),
    ('DIFERENTE',  r'!='),
    ('MAIOR_IGUAL', r'>='),
    ('MENOR_IGUAL', r'<='),
    ('MAIOR',      r'>'),
    ('MENOR',      r'<'),
    ('DOIS_PONTOS', r':'),
    ('PONTO_VIRG', r';'),
    ('VIRGULA',    r','),
    ('ABRE_PAR',   r'\('),
    ('FECHA_PAR',  r'\)'),
    ('MAIS',       r'\+'),
    ('MENOS',      r'-'),
    ('VEZES',      r'\*'),
    ('DIVIDIDO',   r'/'),
    ('SKIP',       r'[ \t\n]+'),
    ('MISMATCH',   r'.'),
]

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', linha {self.line})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_line = 1
        self.tokenize()

    def tokenize(self):
        token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_TYPES)
        get_token = re.compile(token_regex, re.DOTALL).match
        pos = 0
        mo = get_token(self.code)
        
        while mo is not None:
            typ = mo.lastgroup
            val = mo.group(typ)
            
            if typ == 'SKIP':
                self.current_line += val.count('\n')
            elif typ == 'COMENTARIO':
                self.current_line += val.count('\n')
            elif typ == 'MISMATCH':
                raise SyntaxError(f"Erro Léxico: Caractere ilegal '{val}' na linha {self.current_line}")
            else:
                self.tokens.append(Token(typ, val, self.current_line))
            
            pos = mo.end()
            mo = get_token(self.code, pos)
        
        self.tokens.append(Token('EOF', None, self.current_line))