import pytest
from src.lexer import Lexer


lexer = Lexer()
@pytest.mark.parametrize("code, token",
                         [
                            ("10 13.1 add", "add"),
                            ("10 13.1 sub", "sub"),
                            ("10 13.1 mul", "mul"),
                            ("10 13.1 div", "div"),
                            ("10 13.1 mod", "mod"),
                         ])
def test_ops(code, token):
    assert lexer.parse(code.split()) == [('int', '10'), ('float', '13.1'), ('op', token)]


@pytest.mark.parametrize("code, token",
                         [
                            ("dup", "dup"),
                            ("clear", "clear"),
                            ("pop", "pop"),
                            ("roll", "roll"),
                            ("exch", "exch"),
                         ])
def test_stack_ops(code, token):
    assert lexer.parse(code.split()) == [('stack_op', token)]


