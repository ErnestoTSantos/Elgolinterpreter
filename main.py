from lexical_interpreter import ElgolLexer
from syntactic_interpreter import ElgolParser


"""def run_lexical_analysis(code: str):
    print("Análise Léxica:")
    lexer = ElgolLexer()
    tokens = lexer.tokenize(code)

    for token in tokens:
        print(token)
"""

def run_syntactic_analysis(code: str):
    print("\nCode Compile:")
    parser = ElgolParser()
    ast = parser.parse(code)
    print(ast)


def main():
    with open("elgol_file.txt", "r") as file:
        code = file.read()

    #run_lexical_analysis(code)
    run_syntactic_analysis(code)


if __name__ == "__main__":
    main()
