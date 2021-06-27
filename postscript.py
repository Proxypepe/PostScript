import sys
import threading
from src.postscript_src import PS
from src.lexer import Lexer
from src.interpreter import Interpreter

lang = PS()

if __name__ == '__main__':
    if sys.argv[1:]:
        my_thread = threading.Thread(target=lang.draw)
        my_thread.start()
        inter = Interpreter(sys.argv[1])
        code = inter.parse_file()
        lang.execute(code)
        lang.end_drawing()
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
            elif source == "draw run":
                file = input("Enter file path: ")
                my_thread = threading.Thread(target=lang.draw)
                my_thread.start()
                lang.start_drawing()
                inter = Interpreter(file)
                code = inter.parse_file()
                print(code)
                lang.execute(code)
                lang.end_drawing()
            else:
                lexer = Lexer()
                ast = lexer.parse(source.split())
                # print("parsed: ", ast)
                lang.execute(ast)
