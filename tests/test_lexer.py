import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lexical_interpreter import ElgolLexer

class TestElgolLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = ElgolLexer()

    def test_reserved_words(self):
        """Testa o reconhecimento de palavras reservadas"""
        tokens = self.lexer.tokenize("elgio inteiro zero comp enquanto se entao senao inicio fim maior menor igual diferente x")
        token_types = [token.type for token in tokens]
        expected = [
            'ELGIO', 'INTEIRO', 'ZERO', 'COMP', 'ENQUANTO', 'SE', 'ENTAO', 'SENAO',
            'INICIO', 'FIM', 'MAIOR', 'MENOR', 'IGUAL', 'DIFERENTE', 'TIMES'
        ]
        self.assertEqual(token_types, expected)

    def test_operators(self):
        """Testa o reconhecimento de operadores"""
        tokens = self.lexer.tokenize("= + - x / . ( )")
        token_types = [token.type for token in tokens]
        expected = ['EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'DOT', 'LPAREN', 'RPAREN']
        self.assertEqual(token_types, expected)

    def test_identifiers(self):
        """Testa o reconhecimento de identificadores válidos"""
        tokens = self.lexer.tokenize("Var Teste ABC")
        token_types = [token.type for token in tokens]
        self.assertEqual(token_types, ['IDENTIFIER'] * 3)

    def test_integers(self):
        """Testa o reconhecimento de inteiros"""
        tokens = self.lexer.tokenize("123 456789 1")
        token_types = [token.type for token in tokens]
        self.assertEqual(token_types, ['INTEGER'] * 3)

    def test_comments(self):
        """Testa a ignorância de comentários"""
        tokens = self.lexer.tokenize("# Comentário\nVar # Outro comentário")
        token_types = [token.type for token in tokens]
        self.assertEqual(token_types, ['IDENTIFIER'])

    def test_comma_outside_parentheses(self):
        """Testa a rejeição de vírgulas fora de parênteses"""
        tokens = self.lexer.tokenize("Var1, Var2")
        token_types = [token.type for token in tokens]
        # A vírgula deve ser ignorada, apenas os identificadores devem permanecer
        self.assertEqual(token_types, ['IDENTIFIER', 'IDENTIFIER'])

    def test_comma_inside_parentheses(self):
        """Testa a aceitação de vírgulas dentro de parênteses"""
        tokens = self.lexer.tokenize("(Var1, Var2)")
        token_types = [token.type for token in tokens]
        self.assertEqual(token_types, ['LPAREN', 'IDENTIFIER', 'COMMA', 'IDENTIFIER', 'RPAREN'])

if __name__ == '__main__':
    unittest.main()