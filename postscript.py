import sys
from src.postscript_src import PS, parse
from src.interpreter import Interpreter

lang = PS()

if __name__ == '__main__':
    if sys.argv[1:]:
        inter = Interpreter(sys.argv[1])
        inter.parse_file()

    else:
        while True:
            source = input(">> ")
            if source == "exit()" or source == "quit()":
                sys.exit()
            elif source == "stack":
                print(lang.stack)
            elif source == "vars":
                print(lang.words)
            elif source == "run":
                file = input("Enter file path: ")
                inter = Interpreter(file)
                inter.parse_file()
            else:
                ast = parse(source.split())
                lang.execute(ast)
                res = lang.result()
                print(res)
