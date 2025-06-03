import ply.lex as lex

from tokens import token_names
from tokens import reserved_words


class ElgolLexer:
    """
    A lexer for the Elgol programming language, implemented using the PLY (Python Lex-Yacc) library.

    This class performs lexical analysis of Elgol source code, converting it into a sequence
    of tokens. These tokens can then be processed by a parser or other tools. Tokens are defined
    based on regular expressions and include operators, identifiers, reserved words, literals,
    comments, and other language elements. It also handles invalid characters and tracks
    parentheses balance.

    Attributes:
    - `tokens` (list): A list of token names recognized by the lexer.
    - `reserved_map` (dict): A mapping of reserved words to their token types.
    - `t_ignore` (str): Characters to be ignored by the lexer (spaces and tabs).
    - `paren_count` (int): A counter to track the balance of open parentheses.
    - `lexer` (lex.Lexer): The PLY lexer instance.
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
        """Initializes the ElgolLexer, creating the PLY lexer instance."""
        self.lexer = lex.lex(module=self)
        self.paren_count = 0

    def input(self, data: str):
        """
        Feeds input data to the lexer and resets internal state.

        Args:
            data (str): The input string to be tokenized.
        """
        self.lexer.input(data)
        self.paren_count = 0
        self.lexer.lineno = 1

    def token(self):
        """
        Returns the next token from the input stream.

        Returns:
            lex.LexToken or None: The next token, or None if end of input.
        """
        return self.lexer.token()

    def tokenize(self, data: str):
        """
        Tokenizes the given data string and returns a list of all tokens.

        Args:
            data (str): The input string to be tokenized.

        Returns:
            list: A list of lex.LexToken objects.
        """
        self.input(data)
        return list(iter(self.token, None))

    def t_COMMENT(self, t):
        r"\#.*"
        """Lexer rule for comments. Ignores characters from '#' to the end of the line."""
        pass

    def t_LPAREN(self, t):
        r"\("
        """Lexer rule for left parenthesis. Tracks parenthesis balance."""
        self.paren_count += 1
        return t

    def t_RPAREN(self, t):
        r"\)"
        """Lexer rule for right parenthesis. Tracks parenthesis balance."""
        if self.paren_count > 0:
            self.paren_count -= 1
        return t

    def t_COMMA(self, t):
        r","
        """
        Lexer rule for comma. Valid only within parentheses.
        Reports a lexical error and discards the token if a comma is found outside parentheses.
        """
        if self.paren_count > 0:
            return t
        else:
            print(
                f"Lexical Error: Unexpected comma '{t.value}' outside parentheses on line {t.lineno}, column {self._find_column(t.lexer.lexdata, t)}."
            )
            return None

    def t_FUNCTION_NAME(self, t):
        r"_[A-Z][A-Za-zÀ-ÖØ-öø-ÿ][A-Za-z0-9À-ÖØ-öø-ÿ]*"
        """
        Lexer rule for Elgol function names.
        Function names must start with '_' followed by an uppercase letter,
        and then at least two more ASCII alphanumeric characters.
        Reports a lexical error and discards the token if the format is invalid.
        """
        name_part_candidate = t.value[1:]
        is_valid_function_name = True

        if not (len(name_part_candidate) >= 3):
            is_valid_function_name = False

        if is_valid_function_name and not name_part_candidate.isascii():
            is_valid_function_name = False

        if is_valid_function_name and not name_part_candidate.isalnum():
            is_valid_function_name = False

        if is_valid_function_name:
            t.type = "FUNCTION_NAME"
            return t
        else:
            print(
                f"Lexical Error: Malformed Elgol function name or invalid characters '{t.value}' on line {t.lineno}, column {self._find_column(t.lexer.lexdata, t)}."
            )
            return None

    def t_INTEGER(self, t):
        r"[1-9][0-9]*"
        """Lexer rule for integer literals (non-zero starting). Converts the matched string to an integer."""
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-z0-9À-ÖØ-öø-ÿ]*"
        """
        Lexer rule for identifiers and reserved words.
        If the token is a reserved word, its type is set accordingly.
        Otherwise, it's validated as an Elgol identifier (starts with uppercase,
        length >= 3, ASCII, and alphanumeric).
        Reports a lexical error and discards the token if it's an invalid identifier.
        """
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
                f"Lexical Error: Invalid Elgol reserved word or identifier '{t.value}' on line {t.lineno}, column {self._find_column(t.lexer.lexdata, t)}."
            )
            return None

    def t_newline(self, t):
        r"\n+"
        """Lexer rule for newlines. Updates the line number."""
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        """
        Lexer rule for handling lexical errors (invalid characters).
        Prints an error message and skips the invalid character.
        """
        print(
            f"Lexical Error: Invalid character '{t.value[0]}' on line {t.lineno}, column {self._find_column(t.lexer.lexdata, t)}."
        )
        t.lexer.skip(1)

    def _find_column(self, text_input: str, token_or_lexer_instance) -> int:
        """
        Calculates the column number of a token within the input text.

        Args:
            text_input (str): The full input string.
            token_or_lexer_instance (lex.LexToken or lex.Lexer): The token or lexer instance
                                                                for which to find the column.

        Returns:
            int: The column number (1-based).
        """
        lexpos = token_or_lexer_instance.lexpos
        line_start = text_input.rfind("\n", 0, lexpos) + 1
        return (lexpos - line_start) + 1