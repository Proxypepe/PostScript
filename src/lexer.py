from typing import Union, List, Tuple
from src import Errno


class Lexer:
    """
    Lexer Class -
    Parses the code into tokens, then classifies them
    """

    def __init__(self):
        # Built-in keywords
        self.op = ("add", "sub", "mul", "div", "mod", "neg")
        self.stack_op = ("dup", "clear", "pop", "roll", "exch")
        self.logic = ("eq", "gt", "ge", "ne", "lt", "le")
        self.logical_op = ("not", "and", "xor", "or")
        self.basic_keywords = ("if", "ifelse", "for", "array", "def")
        self.draw = ("moveto", "lineto")
        self.data_types = ("int", "float")
        self.ex = "executable_array"
        self.bars_enum = ('{', '}')

        # stacks for checking bars
        self.bars = []
        self.sq_bars = []

        # support vars
        self.is_array = False
        self.is_comment = False


    def identify_type(self, token: Union[int, float, str]) -> str:
        """
        Classifies the input token and returns the data type in string format

        :param token: Union[int, float, str]
        :return: str -
        Returns datatype
        """
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

    @Errno.ErrorTrace
    def parse(self, tokens, code=None) -> list[tuple]:
        if code is None:
            code = []
        for i, token in enumerate(tokens):
            if self.identify_type(token) in self.data_types:
                data_type = self.identify_type(token)
                code.append((data_type, token))
            elif token == '':
                pass
            elif token == "/*":
                self.is_comment = True
                # code.append(("comment", token))
            elif token == "*/":
                self.is_comment = False
                # code.append(("comment", token))
            elif self.is_comment:
                pass
                # code.append(("comment", token))
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
                    raise Errno.InvalidBars()
            elif token == "[" and self.is_array:
                self.sq_bars.append('[')
                code.append(("open_array", token))
            elif token == "]" and self.is_array:
                self.sq_bars.pop()
                code.append(("close_array", token))
            elif "[" in token and token[-1] == "]":
                open_b = token.find('[')
                code.append(("array", token[:open_b]))
                code.append(("access_op", token[open_b:]))
            else:
                code.append(("var", token))
        if self.bars or self.sq_bars:
            raise Errno.InvalidBars(0)
        return code
