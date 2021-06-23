import sys
import threading
from src.postscript_src import PS
from src.lexer import Lexer
from src.interpreter import Interpreter

lang = PS()

if __name__ == '__main__':
    if sys.argv[1:]:
        inter = Interpreter(sys.argv[1])
        code = inter.parse_file()
        lang.execute(code)

    else:
        my_thread = None
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
                code = inter.parse_file()
                lang.execute(code)
            elif source == "draw":
                my_thread = threading.Thread(target=lang.draw)
                my_thread.start()
            elif source == "draw run":
                file = input("Enter file path: ")
                my_thread = threading.Thread(target=lang.draw)
                my_thread.start()
                inter = Interpreter(file)
                code = inter.parse_file()
                lang.execute(code)
            else:
                lexer = Lexer()
                ast = lexer.parse(source.split())
                print("parsed: ", ast)
                lang.execute(ast)
                res = lang.result()
                print(res)
