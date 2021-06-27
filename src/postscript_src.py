import turtle
from src import Errno
from src.lexer import Lexer


class PS:
    def __init__(self):
        self.stack = []
        self.bars = 0
        self.lexer = Lexer()
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

            'not': self.logic_not,
            'and': self.logic_and,
            'or': self.logic_or,
            'xor': self.logic_xor,

            # Built-in keywords
            'if': self.core_if,
            'ifelse': self.core_ifelse,
            'for': self.core_for,
            'array': self.core_array,

            'def': self.define,
            'access_op': self.access_op,

            # Built-in functions
            'print': self.built_print,

        }

        self.draw_words = {
            'moveto': self.draw_moveto,
            'lineto': self.draw_lineto
        }

        self.pen = None
        self.drawing_window = None

    @Errno.ErrorTrace
    def execute(self, code):
        for type_, word in code:
            if type_ == "int":
                self.stack.append(int(word))
            elif type_ == "float":
                self.stack.append(float(word))
            # elif type_ == "comment":
            #     pass
            elif type_ == "var_create":
                self.words[word] = None
                self.stack.append(word)
            elif type_ == "array":
                self.stack.append(word)
            elif type_ == "access_op":
                self.stack.append(word)
                self.access_op()
            elif type_ == "draw" and self.pen is not None:
                self.draw_words[word]()
            elif type_ == "var":
                if self.words[word] is None:
                    self.stack.append(word)
                elif type(self.words[word]) == list:
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

    def logic_not(self):
        op = self.stack.pop()
        self.stack.append(int(not op))

    def logic_and(self):
        op1 = self.stack.pop()
        op2 = self.stack.pop()
        self.stack.append(op1 & op2)

    def logic_or(self):
        op1 = self.stack.pop()
        op2 = self.stack.pop()
        self.stack.append(op1 | op2)

    def logic_xor(self):
        op1 = self.stack.pop()
        op2 = self.stack.pop()
        self.stack.append(op1 ^ op2)

    def core_if(self):
        self.stack.pop()
        code = self.create_execute_array()
        tmp = self.stack.pop()
        if tmp == 1:
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
            code = self.lexer.parse(op1)
        elif tmp == 0:
            op2.reverse()
            code = self.lexer.parse(op2)
        self.execute(code)

    def core_for(self):
        self.stack.pop()
        code = self.create_execute_array()
        stop = self.stack.pop()
        step = self.stack.pop()
        start = self.stack.pop()
        for _ in range(start, stop, step):
            self.execute(code)

    def core_array(self):
        pass

    def define(self):
        value = self.stack.pop()
        if value != "}" and value != "]":
            name = self.stack.pop()
            self.words[name] = value
        elif value == "}":
            code = self.create_execute_array()
            name = self.stack.pop()
            self.words[name] = code
        elif value == "]":
            array = self.create_array()
            name = self.stack.pop()
            array.reverse()
            self.words[name] = array

    def access_op(self):
        index = self.stack.pop()
        index = index[1:-1]
        if not index.isdigit():
            raise Errno.InvalidIndex()
        index = int(index)
        var = self.stack.pop()
        if var not in self.words:
            raise Errno.UnknownVariable()
        if index > len(self.words[var]):
            raise Errno.InvalidIndex()
        self.stack.append(self.words[var][index][1])

    def result(self):
        if len(self.stack) != 0:
            res = self.stack[-1]
            return res
        else:
            return ""

    def create_execute_array(self):
        bars = 1
        code = []
        op = self.stack.pop()
        while bars != 0:
            code.append(op)
            op = self.stack.pop()
            if op == "{":
                bars -= 1
            elif op == "}":
                bars += 1
        code.reverse()
        code = self.lexer.parse(code)
        return code

    def create_array(self):
        token = self.stack.pop()
        array = []
        while token != '[':
            _type = self.lexer.identify_type(token)
            array.append((_type, token))
            token = self.stack.pop()
        return array

    def built_print(self):
        args = self.stack.pop()
        if type(args) != int:
            raise Errno.InvalidFuncArgs
        res = []
        for _ in range(args):
            res.append(self.stack.pop())
        res.reverse()
        print(*res)

    # Drawing part implementation
    def draw(self):
        self.drawing_window = turtle.Screen()
        self.drawing_window.title("PostScript")

    def start_drawing(self):
        self.pen = turtle.Turtle()

    def end_drawing(self):
        turtle.mainloop()

    def draw_moveto(self):
        self.pen.up()
        y = self.stack.pop()
        x = self.stack.pop()
        self.pen.goto(x, y)

    def draw_lineto(self):
        self.pen.down()
        y = self.stack.pop()
        x = self.stack.pop()
        self.pen.goto(x, y)


if __name__ == '__main__':
    source = '5 dup 1 add 2 div mul'
    ps = PS()
    l = Lexer()
    ast = l.parse(source.split())
    print(ast)
    ps.execute(ast)
    print(ps.stack)
