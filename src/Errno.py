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
        except PSExceptionStream:
            print(PSExceptionStream())
            sys.exit()
    return wrapper


class PSExceptionStream(Exception):
    """PS Base Exception class """
    def __init__(self, msg=None):
        pass

    def __str__(self):
        return """Base Exception class in PS"""

    def __repr__(self):
        return """Base Exception class in PS"""


class InvalidBars(PSExceptionStream):
    """Invalid number of braces
    """
    def __init__(self):
        pass

    def __str__(self):
        return """Invalid number of braces"""

    def __repr__(self):
        return """Invalid number of braces"""


class InvalidIndex(PSExceptionStream):
    """

    """
    pass


class OutOfRange(PSExceptionStream):
    pass


class UnknownVariable(PSExceptionStream):
    pass
