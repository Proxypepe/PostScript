from src.postscript_src import PS, parse
import os.path


class Interpreter:
    def __init__(self, filename):
        self.lang = PS()
        self.file = filename

    def parse_file(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                code = []
                for line in f:
                    format_line = line.split(" ")
                    tmp = format_line.pop()
                    format_line.append(tmp[:-1]) if "\n" in tmp else format_line.append(tmp)
                    # print(f"line {format_line}")
                    code += parse(format_line)
                    # print(f"code {code}")
                    # print(self.lang.stack)
                # print(self.lang.result())
                # print(self.lang.words)
            return code
        else:
            print("Error file name")
