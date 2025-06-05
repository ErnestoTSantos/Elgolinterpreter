# import unittest
# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from syntactic_interpreter import ElgolParser

# class TestElgolParser(unittest.TestCase):
#     def setUp(self):
#         self.parser = ElgolParser()

#     def parse_code(self, code):
#         """Helper method to parse code and return AST or None"""
#         return self.parser.parse(code)

#     def test_empty_program(self):
#         """Testa um programa vazio"""
#         ast = self.parse_code("")
#         self.assertEqual(ast, ("program", []))

#     def test_simple_program(self):
#         """Testa um programa simples com declaração e atribuição"""
#         code = """
#         inicio.
#             inteiro Var.
#             Var = 123.
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         self.assertEqual(ast[0], "program")
#         # Verifica se há uma declaração e uma atribuição
#         block = ast[1][0][1]  # program -> component_list -> block
#         statements = block[1]  # block -> statement_list
#         self.assertEqual(len(statements), 2)

#     def test_function_definition(self):
#         """Testa a definição de uma função"""
#         code = """
#         inteiro _Funcao(inteiro Param1, inteiro Param2).
#         inicio.
#             Param1 = Param2 + 1.
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         self.assertEqual(ast[1][0][0], "function_definition")

#     def test_if_statement(self):
#         """Testa a estrutura if-then"""
#         code = """
#         inicio.
#             inteiro Var.
#             se Var maior zero.
#             entao.
#             inicio.
#                 Var = 1.
#             fim.
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         block = ast[1][0][1]  # program -> component_list -> block
#         statements = block[1]  # block -> statement_list
#         self.assertEqual(statements[1][0], "if_statement")

#     def test_while_statement(self):
#         """Testa a estrutura while"""
#         code = """
#         inicio.
#             inteiro Var.
#             enquanto Var maior zero.
#             inicio.
#                 Var = Var - 1.
#             fim.
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         block = ast[1][0][1]  # program -> component_list -> block
#         statements = block[1]  # block -> statement_list
#         self.assertEqual(statements[1][0], "while_statement")

#     def test_function_call(self):
#         """Testa chamada de função"""
#         code = """
#         inicio.
#             inteiro Var.
#             Var = _Funcao(1, 2).
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         block = ast[1][0][1]  # program -> component_list -> block
#         statements = block[1]  # block -> statement_list
#         assignments = [stmt for stmt in statements if isinstance(stmt, tuple) and stmt[0] == "assign"]
#         self.assertEqual(assignments[0][2][0], "function_call")

#     def test_comma_in_declaration(self):
#         """Testa uso inválido de vírgula em declaração"""
#         code = """
#         inicio.
#             inteiro Var1, Var2.
#         fim.
#         """
#         ast = self.parse_code(code)
#         # Verifica se houve erro de sintaxe
#         self.assertGreater(self.parser.syntax_error_count, 0)

#     def test_invalid_assignment_to_elgio(self):
#         """Testa atribuição inválida a elgio com chamada de função"""
#         code = """
#         inicio.
#             elgio = _Funcao(1, 2).
#         fim.
#         """
#         ast = self.parse_code(code)
#         # Verifica se houve erro de sintaxe
#         self.assertGreater(self.parser.syntax_error_count, 0)

#     def test_invalid_operator_usage(self):
#         """Testa uso inválido de operador (operador sem operandos)"""
#         code = """
#         inicio.
#             inteiro Var.
#             Var = x.
#         fim.
#         """
#         ast = self.parse_code(code)
#         # Verifica se houve erro de sintaxe
#         self.assertGreater(self.parser.syntax_error_count, 0)

#     def test_missing_dot(self):
#         """Testa erro de sintaxe por ponto faltante"""
#         code = """
#         inicio
#             inteiro Var
#             Var = 123
#         fim
#         """
#         ast = self.parse_code(code)
#         # Verifica se houve erro de sintaxe
#         self.assertGreater(self.parser.syntax_error_count, 0)

#     def test_missing_parameter_name(self):
#         """Testa parâmetro de função sem nome"""
#         code = """
#         inteiro _Funcao(inteiro).
#         inicio.
#         fim.
#         """
#         ast = self.parse_code(code)
#         # Verifica se houve erro de sintaxe
#         self.assertGreater(self.parser.syntax_error_count, 0)

#     def test_nested_blocks(self):
#         """Testa blocos aninhados"""
#         code = """
#         inicio.
#             inteiro Var.
#             se Var maior zero.
#             entao.
#             inicio.
#                 enquanto Var maior zero.
#                 inicio.
#                     Var = Var - 1.
#                 fim.
#             fim.
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         # Verifica a estrutura aninhada
#         block = ast[1][0][1]  # program -> component_list -> block
#         statements = block[1]  # block -> statement_list
#         if_stmt = statements[1]  # if_statement
#         inner_block = if_stmt[1]["then_block"]  # then_block
#         inner_statements = inner_block[1]  # statement_list inside then_block
#         while_stmt = inner_statements[0]  # while_statement
#         self.assertEqual(while_stmt[0], "while_statement")

#     def test_unary_operator(self):
#         """Testa operador unário comp"""
#         code = """
#         inicio.
#             inteiro Var.
#             Var = comp 1.
#         fim.
#         """
#         ast = self.parse_code(code)
#         self.assertIsNotNone(ast)
#         block = ast[1][0][1]  # program -> component_list -> block
#         statements = block[1]  # block -> statement_list
#         assignments = [stmt for stmt in statements if isinstance(stmt, tuple) and stmt[0] == "assign"]
#         self.assertEqual(assignments[0][2][0], "unary_operator_comp")

# if __name__ == '__main__':
#     unittest.main()