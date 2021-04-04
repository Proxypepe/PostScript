
def parse(tokens, code=None):
    if code is None:
        code = []
    op = ("add", "sub", "mul", "div", "mod", "neg")
    stack_op = ("dup", "clear", "pop", "roll", "exch")
    logic = ("eq", "gt", "ge", "ne", "lt", "le")
    logical_op = ("not", "and", "xor", "or")
    basic_keywords = ("if", "ifelse", "for", "array", "def")
    draw = ("moveto", "lineto")
    num = "int", "float"
    for token in tokens:
        if type(token) == int or token.isdigit():
            code.append((num[0], token))
        elif token == '':
            pass
        elif token in op:
            code.append(("op", token))
        elif token in stack_op:
            code.append(("stack_op", token))
        elif token in logic:
            code.append(("logic", token))
        elif token in basic_keywords:
            code.append(("basic_keywords", token))
        elif token in logical_op:
            code.append(("logical_op", token))
        elif token in draw:
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
