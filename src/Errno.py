import sys


def ErrorTrace(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print("Invalid syntax")
            sys.exit()
        except KeyError:
            print("Invalid var")
            sys.exit()
        except InvalidBars:
            print(InvalidBars())
            sys.exit()
    return wrapper


class InvalidBars(Exception):
    """Invalid number of braces
    """
    def __str__(self):
        return """Invalid number of braces"""

    def __repr__(self):
        return """Invalid number of braces"""


class InvalidIndex(Exception):
    """

    """
    pass


class OutOfRange(Exception):
    pass


class UnknownVariable(Exception):
    pass
