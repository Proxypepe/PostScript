import src.Errno as errno


class Lexer:
    def __init__(self):
        self.op = ("add", "sub", "mul", "div", "mod", "neg")
        self.stack_op = ("dup", "clear", "pop", "roll", "exch")
        self.logic = ("eq", "gt", "ge", "ne", "lt", "le")
        self.logical_op = ("not", "and", "xor", "or")
        self.basic_keywords = ("if", "ifelse", "for", "array", "def")
        self.draw = ("moveto", "lineto")
        self.data_types = ("int", "float")
        self.ex = "executable_array"
        self.bars_enum = ('{', '}')

        self.bars = []

        self.is_array = False

    def identify_type(self, token) -> str:
        if type(token) == int:
            return "int"
        elif type(token) == float:
            return "float"
        elif token.isdigit():
            return "int"
        elif len(token.split('.')) == 2:
            return "float"
        elif '"' in token:
            return "str"
        return "Unknown type"

    def parse(self, tokens, code=None):
        if code is None:
            code = []
        for i, token in enumerate(tokens):
            if self.identify_type(token) in self.data_types:
                data_type = self.identify_type(token)
                code.append((data_type, token))
            elif token == '':
                pass
            elif token in self.op:
                code.append(("op", token))
            elif token in self.stack_op:
                code.append(("stack_op", token))
            elif token in self.logic:
                code.append(("logic", token))
            elif token in self.basic_keywords:
                if token == "def":
                    self.is_array = False
                code.append(("basic_keywords", token))
            elif token in self.logical_op:
                code.append(("logical_op", token))
            elif token in self.draw:
                code.append(("draw", token))
            elif token[0] == "/":
                # TODO check keywords
                self.is_array = True
                code.append(("var_create", token[1:]))
            elif token == "{":
                code.append(("open", token))
                self.bars.append("{")
            elif token == "}":
                code.append(("close", token))
                if self.bars:
                    self.bars.pop()
                else:
                    raise errno.InvalidBars(i)
            elif token == "[" and self.is_array:
                code.append(("open_array", token))
            elif token == "]" and self.is_array:
                code.append(("close_array", token))
            else:
                code.append(("var", token))
        if self.bars:
            raise errno.InvalidBars(0)
        return code
