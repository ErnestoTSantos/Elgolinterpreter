import ply.yacc as yacc

from lexical_interpreter import ElgolLexer


class ElgolParser:
    def __init__(self):
        self.lexer_instance = ElgolLexer()
        self.tokens = self.lexer_instance.tokens
        self.parser = yacc.yacc(module=self, start="program", debug=True, outputdir=".")

    precedence = (
        ("right", "EQUALS"),
        ("left", "IGUAL", "DIFERENTE"),
        ("left", "MAIOR", "MENOR"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
        ("right", "P_UNARY_COMP"),
    )

    start = "program"

    def p_program(self, p):
        """program : component_list"""
        p[0] = ("program", p[1] if p[1] is not None else [])

    def p_component_list(self, p):
        """component_list : component_list component
        | component
        | empty"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            p[0] = p[1] + ([p[2]] if p[2] is not None else [])

    def p_component(self, p):
        """component : function_definition
        | main_block"""
        p[0] = p[1]

    def p_function_definition(self, p):
        """function_definition : type_specifier FUNCTION_NAME LPAREN parameters_opt RPAREN DOT block"""
        p[0] = (
            "function_definition",
            {"type": p[1], "name": p[2], "params": p[4], "body": p[7]},
        )

    def p_parameters_opt(self, p):
        """parameters_opt : parameter_list
        | empty"""
        p[0] = p[1] if p[1] is not None else []

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA parameter
        | parameter"""
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_parameter(self, p):
        """parameter : type_specifier IDENTIFIER"""
        p[0] = ("parameter", {"type": p[1], "name": p[2]})

    def p_type_specifier(self, p):
        """type_specifier : INTEIRO"""
        p[0] = p[1]

    def p_main_block(self, p):
        """main_block : block"""
        p[0] = ("main_block", p[1])

    def p_block(self, p):
        """block : INICIO DOT statement_list_opt FIM DOT"""
        p[0] = ("block", p[3])

    def p_statement_list_opt(self, p):
        """statement_list_opt : statement_list
        | empty"""
        p[0] = p[1] if p[1] is not None else []

    def p_statement_list(self, p):
        """statement_list : statement_list statement
        | statement"""
        if len(p) == 3:
            new_statement_node = p[2]
            p[0] = p[1] + (
                [new_statement_node] if new_statement_node is not None else []
            )
        else:
            p[0] = [p[1]] if p[1] is not None else []

    def p_variable_declaration(self, p):
        """variable_declaration : type_specifier IDENTIFIER"""
        p[0] = ("variable_declaration", {"type": p[1], "name": p[2]})

    def p_statement(self, p):
        """statement : variable_declaration DOT
        | expression_statement DOT
        | if_statement
        | while_statement"""
        p[0] = p[1]

    def p_expression_statement(self, p):
        """expression_statement : expression"""
        p[0] = p[1]

    def p_if_statement(self, p):
        """if_statement : SE expression DOT ENTAO DOT block senao_opt"""
        p[0] = (
            "if_statement",
            {"condition": p[2], "then_block": p[6], "else_block": p[7]},
        )

    def p_senao_opt(self, p):
        """senao_opt : SENAO DOT block
        | empty"""
        if len(p) == 4:
            p[0] = p[3]
        else:
            p[0] = None

    def p_while_statement(self, p):
        """while_statement : ENQUANTO expression DOT block"""
        p[0] = ("while_statement", {"condition": p[2], "body": p[4]})

    def p_lvalue(self, p):
        """lvalue : IDENTIFIER
        | ELGIO"""
        p[0] = ("lvalue", p[1])

    def p_expression_assign(self, p):
        """expression : lvalue EQUALS expression"""
        p[0] = ("assign", p[1][1], p[3])

    def p_expression_binop(self, p):
        """expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | expression MAIOR expression
        | expression MENOR expression
        | expression IGUAL expression
        | expression DIFERENTE expression"""
        p[0] = (p[2], p[1], p[3])

    def p_expression_comp_unary(self, p):
        """expression : COMP expression %prec P_UNARY_COMP"""
        p[0] = ("unary_operator_comp", p[2])

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_integer(self, p):
        """expression : INTEGER"""
        p[0] = ("integer_literal", p[1])

    def p_expression_zero(self, p):
        """expression : ZERO"""
        p[0] = ("integer_literal", 0)

    def p_expression_identifier_like(self, p):
        """expression : IDENTIFIER
        | ELGIO"""
        p[0] = ("identifier_lookup", p[1])

    def p_expression_function_call(self, p):
        """expression : FUNCTION_NAME LPAREN argument_list_opt RPAREN"""
        p[0] = ("function_call", p[1], p[3])

    def p_argument_list_opt(self, p):
        """argument_list_opt : argument_list
        | empty"""
        p[0] = p[1] if p[1] is not None else []

    def p_argument_list(self, p):
        """argument_list : argument_list COMMA expression
        | expression"""
        if len(p) == 4:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_empty(self, p):
        """empty :"""
        p[0] = None

    def p_error(self, p):
        if p:
            print(
                f"Erro de sintaxe na linha {p.lineno}: símbolo inesperado '{p.value}'"
            )

            if hasattr(p.lexer, "last_token"):
                last = p.lexer.last_token
                if last.type in ("PLUS", "MINUS", "TIMES", "DIVIDE"):
                    print(
                        f"Erro: operador '{last.value}' sem operando inteiro à direita na linha {last.lineno}"
                    )
        else:
            print("Erro de sintaxe: fim de arquivo inesperado")

    def parse(self, data: str):
        return self.parser.parse(data, lexer=self.lexer_instance.lexer, tracking=True)
