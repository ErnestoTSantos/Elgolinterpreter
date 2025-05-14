from lexical_interpreter import ElgolLexer

def main():
    with open('elgol_file.txt', 'r') as file:
        code = file.read()

    lexer = ElgolLexer()
    tokens = lexer.tokenize(code)

    for token in tokens:
        print(token)

main()