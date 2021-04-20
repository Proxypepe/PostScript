class Lexer:
    def __init__(self):
        self.op = ("add", "sub", "mul", "div", "mod", "neg")
        self.stack_op = ("dup", "clear", "pop", "roll", "exch")
        self.logic = ("eq", "gt", "ge", "ne", "lt", "le")
        self.logical_op = ("not", "and", "xor", "or")
        self.basic_keywords = ("if", "ifelse", "for", "array", "def")
        self.draw = ("moveto", "lineto")
        self.num = ("int", "float")
        self.ex = "executable_array"

    def parse(self, tokens, code=None):
        if code is None:
            code = []
        for token in tokens:
            if type(token) == int or token.isdigit():
                code.append((self.num[0], token))
            elif token == '':
                pass
            elif token in self.op:
                code.append(("op", token))
            elif token in self.stack_op:
                code.append(("stack_op", token))
            elif token in self.logic:
                code.append(("logic", token))
            elif token in self.basic_keywords:
                code.append(("basic_keywords", token))
            elif token in self.logical_op:
                code.append(("logical_op", token))
            elif token in self.draw:
                code.append(("draw", token))
            elif token[0] == "/":
                code.append(("var_creat", token[1:]))
            elif token == "{":
                code.append(("open", token))
            elif token == "}":
                code.append(("close", token))
            else:
                code.append(("var", token))
        return code
