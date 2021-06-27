import pytest
from src.postscript_src import PS

lang = PS()


@pytest.mark.parametrize("code",
                         [
                            [('int', '25'), ('int', '25'), ('op', 'add')],
                            [('int', '75'), ('int', '25'), ('op', 'sub')],
                            [('int', '25'), ('int', '2'), ('op', 'mul')],
                            [('int', '100'), ('int', '2'), ('op', 'div')],
                            [('int', '150'), ('int', '100'), ('op', 'mod')],
                         ])
def test_ops(code):
    lang.execute(code)
    assert lang.stack[-1] == 50
