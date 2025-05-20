import ply.lex as lex

from tokens import token_names
from tokens import reserved_words


class ElgolLexer:
    tokens = token_names

    t_EQUALS = r'='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'x'
    t_DIVIDE = r'/'
    #t_LPAREN = r'\('
    #t_RPAREN = r'\)'
    t_DOT = r'\.'
    #t_COMMA = r','

    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.paren_count = 0

    def input(self, data: str):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def tokenize(self, data: str):
        self.input(data)
        return list(iter(self.token, None))

    # Comentários
    def t_COMMENT(self, t):
        r'\#.*'
        pass
    
    # Parênteses
    def t_LPAREN(self, t):
        r'\('
        self.paren_count += 1
        return t

    def t_RPAREN(self, t):
        r'\)'
        if self.paren_count > 0:
            self.paren_count -= 1
        return t

    # Comma (apenas entre parênteses)
    def t_COMMA(self, t):
        r','
        if self.paren_count > 0:
            return t
        else:
            t.type = 'ERROR'
            t.value = t.value
            return self.t_error(t)

    # Função válida: _ + identificador válido
    def t_FUNCTION_NAME(self, t):
        r'_[A-Z][a-zA-Z]{2,}'
        return t

    # Identificadores válidos
    def t_ID(self, t):
        r'[A-Za-z]{3,}'
        if t.value in reserved_words:
            t.type = reserved_words[t.value]
        elif t.value.startswith('_') and len(t.value) > 1 and t.value[1:].isalpha() and t.value[1].isupper() and len(
                t.value[1:]) >= 3:
            t.type = 'FUNCTION_NAME'
        elif t.value[0].isupper() and t.value.isalpha() and len(t.value) >= 3:
            t.type = 'IDENTIFIER'
        else:
            t.lexer.skip(len(t.value))
            return None
        return t

    # Inteiros
    def t_INTEGER(self, t):
        r'[1-9][0-9]*'
        t.value = int(t.value)
        return t

    # Quebra de linha
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Erro léxico
    def t_error(self, t):
        print(f"Caractere inválido: '{t.value[0]}' na linha {t.lineno}")
        t.lexer.skip(1)
