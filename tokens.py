reserved_words = {
    'elgio': 'ELGIO',
    'inteiro': 'INTEIRO',
    'zero': 'ZERO',
    'comp': 'COMP',
    'enquanto': 'ENQUANTO',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'inicio': 'INICIO',
    'fim': 'FIM',
    'maior': 'MAIOR',
    'menor': 'MENOR',
    'igual': 'IGUAL',
    'diferente': 'DIFERENTE'
}

token_names = [
    'ID',
    'IDENTIFIER',
    'FUNCTION_NAME',
    'INTEGER',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'DOT',
] + list(reserved_words.values())
