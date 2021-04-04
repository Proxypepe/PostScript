from src import Errno


def parse(tokens, code=None):
    if code is None:
        code = []
    op = ("add", "sub", "mul", "div", "mod", "neg")
    stack_op = ("dup", "clear", "pop", "roll", "exch")
    logic = ("eq", "gt", "ge", "ne", "lt", "le")
    logical_op = ("not", "and", "xor")
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
        elif token in logical_op:
            code.append(("logical_op", token))
        elif token[0] == "/":
            code.append(("var_creat", token[1:]))
        elif token == "{":
            code.append(("open", token))
        elif token == "}":
            code.append(("close", token))
        elif token == "def":
            code.append(("def", token))
        elif token == "if":
            code.append(("if", token))
        elif token == "ifelse":
            code.append(("ifelse", token))
        else:
            code.append(("var", token))
    return code


class PS:
    def __init__(self):

        self.stack = []
        self.bars = 0
        self.words = {
            # arithmetic
            'add': self.op_add,
            'sub': self.op_sub,
            'mul': self.op_mul,
            'div': self.op_div,
            'mod': self.op_mod,
            'neg': self.op_neg,

            # stack
            'dup': self.stack_dup,
            'clear': self.stack_clear,
            'pop': self.stack_pop,
            'roll': self.stack_roll,
            'exch': self.stack_exch,

            # logic
            'eq': self.logic_eq,
            'gt': self.logic_gt,
            'ge': self.logic_ge,
            'ne': self.logic_ne,
            'lt': self.logic_lt,
            'le': self.logic_le,

            # another keywords
            'if': self.core_if,
            'ifelse': self.core_ifelse,

            'def': self.define,
        }

    @Errno.VarTrace
    @Errno.IndexTrace
    def execute(self, code):
        for type_, word in code:
            if type_ == "int":
                self.stack.append(int(word))
            elif type_ == "var_creat":
                self.words[word] = None
                self.stack.append(word)
            elif type_ == "var":
                if type(self.words[word]) == list:
                    self.execute(self.words[word])
                else:
                    self.stack.append(self.words[word])
            elif type_ == "open":
                self.bars += 1
                self.stack.append(word)
            elif type_ == "close":
                self.bars -= 1
                self.stack.append(word)
            elif word in self.words and self.bars == 0:
                self.words[word]()
            else:
                self.stack.append(word)

    def op_neg(self):
        result = int(self.stack.pop()) * -1
        self.stack.append(result)

    def op_add(self):
        _operand1 = self.stack.pop()
        _operand2 = self.stack.pop()
        _result = _operand1 + _operand2
        self.stack.append(_result)

    def op_sub(self):
        _operand1 = self.stack.pop()
        _operand2 = self.stack.pop()
        _result = _operand1 - _operand2
        self.stack.append(_result)

    def op_mul(self):
        _operand1 = self.stack.pop()
        _operand2 = self.stack.pop()
        _result = _operand1 * _operand2
        self.stack.append(_result)

    def op_div(self):
        _operand1 = self.stack.pop()
        _operand2 = self.stack.pop()
        _result = _operand2 // _operand1
        self.stack.append(_result)

    def op_mod(self):
        _operand1 = self.stack.pop()
        _operand2 = self.stack.pop()
        _result = _operand2 % _operand1
        self.stack.append(_result)

    def stack_dup(self):
        self.stack.append(self.stack[-1])

    def stack_clear(self):
        self.stack.clear()

    def stack_pop(self):
        self.stack.pop()

    def stack_roll(self):
        pass  # TODO

    def stack_exch(self):
        first = self.stack.pop()
        second = self.stack.pop()
        self.stack.append(first)
        self.stack.append(second)

    def logic_eq(self):
        left = self.stack.pop()
        right = self.stack.pop()
        self.stack.append(1) if left == right else self.stack.append(0)

    def logic_gt(self):
        left = self.stack.pop()
        right = self.stack.pop()
        self.stack.append(1) if left < right else self.stack.append(0)

    def logic_ge(self):
        left = self.stack.pop()
        right = self.stack.pop()
        self.stack.append(1) if left <= right else self.stack.append(0)

    def logic_ne(self):
        left = self.stack.pop()
        right = self.stack.pop()
        self.stack.append(1) if left != right else self.stack.append(0)

    def logic_lt(self):
        left = self.stack.pop()
        right = self.stack.pop()
        self.stack.append(1) if left > right else self.stack.append(0)

    def logic_le(self):
        left = self.stack.pop()
        right = self.stack.pop()
        self.stack.append(1) if left >= right else self.stack.append(0)

    def core_if(self):
        print(self.stack)
        op1 = []
        tmp = self.stack.pop()
        while tmp != "{":
            if tmp != "}":
                op1.append(tmp)
            tmp = self.stack.pop()
        tmp = self.stack.pop()
        code = []
        if tmp == 1:
            op1.reverse()
            code = parse(op1)
            self.execute(code)

    def core_ifelse(self):
        op1 = []
        op2 = []
        tmp = self.stack.pop()
        while tmp != "{":
            if tmp != "}":
                op2.append(tmp)
            tmp = self.stack.pop()

        tmp = self.stack.pop()
        while tmp != "{":
            if tmp != "}":
                op1.append(tmp)
            tmp = self.stack.pop()

        tmp = self.stack.pop()
        code = []
        if tmp == 1:
            op1.reverse()
            code = parse(op1)
        elif tmp == 0:
            op2.reverse()
            code = parse(op2)
        self.execute(code)

    def define(self):
        value = self.stack.pop()
        if value != "}":
            name = self.stack.pop()
            self.words[name] = value
        elif value == "}":
            # print(self.stack)
            code = []
            op = self.stack.pop()
            bars = 1
            while bars != 0:
                code.append(op)
                op = self.stack.pop()
                if op == "{":
                    bars -= 1
                elif op == "}":
                    bars += 1
            name = self.stack.pop()
            code.reverse()
            code = parse(code)
            self.words[name] = code

    def result(self):
        if len(self.stack) != 0:
            res = self.stack[-1]
            self.stack.clear()
            return res
        else:
            return ""


if __name__ == '__main__':
    import Errno
    source = '5 dup 1 add 2 div mul'
    ps = PS()
    ast = parse(source.split())
    print(ast)
    ps.execute(ast)
    print(ps.stack)
