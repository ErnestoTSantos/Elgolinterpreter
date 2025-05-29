import ply.lex as lex

from tokens import token_names
from tokens import reserved_words


class ElgolLexer:
    """
    A lexer for the Elgol programming language, implemented using the PLY (Python Lex-Yacc) library.

    The purpose of this class is to perform lexical analysis of source code written in Elgol, converting it into a sequence
    of tokens that can be processed by a parser or other tools. Tokens are defined based on regular expressions and include
    operators, identifiers, reserved words, literals, and other language elements.

    Main functionalities:
    - Tokenization of input strings based on predefined rules.
    - Support for reserved words and valid identifiers.
    - Handling of comments and invalid characters.
    - Tracking of parentheses for syntax validation.

    Attributes:
    - `tokens`: List of token names recognized by the lexer.
    - `t_ignore`: Characters to be ignored during analysis (spaces and tabs).
    - `paren_count`: Counter to track the number of open parentheses.

    Main methods:
    - `input(data)`: Receives an input string for analysis.
    - `token()`: Returns the next token from the input.
    - `tokenize(data)`: Tokenizes the entire input string and returns a list of tokens.
    - Methods starting with `t_`: Define the matching rules for each token type.

    This lexer is designed to be used as part of a compiler or interpreter for the Elgol language.
    """

    tokens = token_names
    reserved_map = reserved_words

    t_EQUALS = r"="
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"x"
    t_DIVIDE = r"/"
    t_DOT = r"\."

    t_ignore = " \t"

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.paren_count = 0

    def input(self, data: str):
        self.lexer.input(data)
        self.paren_count = 0
        self.lexer.lineno = 1

    def token(self):
        return self.lexer.token()

    def tokenize(self, data: str):
        self.input(data)
        return list(iter(self.token, None))

    def t_COMMENT(self, t):
        r"\#.*"
        pass

    def t_LPAREN(self, t):
        r"\("
        self.paren_count += 1
        return t

    def t_RPAREN(self, t):
        r"\)"
        if self.paren_count > 0:
            self.paren_count -= 1
        return t

    def t_COMMA(self, t):
        r","
        if self.paren_count > 0:
            return t
        else:
            print(
                f"Erro Léxico: Vírgula inesperada '{t.value}' fora de parênteses na linha {t.lineno}, coluna {self._find_column(t.lexer.lexdata, t)}."
            )
            return None

    def t_FUNCTION_NAME(self, t):
        r"_[A-Z][a-zA-Z0-9]*"
        name_part_candidate = t.value[1:]
        if len(name_part_candidate) >= 3 and name_part_candidate.isalpha():
            t.type = "FUNCTION_NAME"
            return t
        else:
            print(
                f"Erro Léxico: Nome de função Elgol mal formado ou com caracteres inválidos '{t.value}' na linha {t.lineno}, coluna {self._find_column(t.lexer.lexdata, t)}."
            )
            return None

    def t_INTEGER(self, t):
        r"[1-9][0-9]*"
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-z0-9À-ÖØ-öø-ÿ]*"

        if t.value in self.reserved_map:
            t.type = self.reserved_map[t.value]
            return t

        is_valid_elgol_identifier = True

        if not t.value[0].isupper():
            is_valid_elgol_identifier = False

        if len(t.value) < 3:
            is_valid_elgol_identifier = False

        if not t.value.isascii() or not t.value.isalnum():
            is_valid_elgol_identifier = False

        if is_valid_elgol_identifier:
            t.type = "IDENTIFIER"
            return t
        else:
            print(
                f"Erro Léxico: Palavra reservada ou identificador Elgol inválido '{t.value}' na linha {t.lineno}, coluna {self._find_column(t.lexer.lexdata, t)}."
            )
            return None

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(
            f"Erro Léxico: Caractere inválido '{t.value[0]}' na linha {t.lineno}, coluna {self._find_column(t.lexer.lexdata, t)}."
        )
        t.lexer.skip(1)

    def _find_column(self, text_input, token_or_lexer_instance):
        lexpos = token_or_lexer_instance.lexpos
        line_start = text_input.rfind("\n", 0, lexpos) + 1
        return (lexpos - line_start) + 1
