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
        except PSExceptionStream as e:
            print(e)
            sys.exit()
    return wrapper


class PSExceptionStream(Exception):
    """PS Base Exception class """
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return self.__class__.__name__

    def __repr__(self):
        if self.message:
            return self.message
        return self.__class__.__name__


class InvalidBars(PSExceptionStream):
    """Invalid number of braces"""
    def __init__(self, message=None):
        super(InvalidBars, self).__init__(message)


class InvalidIndex(PSExceptionStream):
    """   """
    def __init__(self, message=None):
        super(InvalidIndex, self).__init__(message)


class OutOfRange(PSExceptionStream):
    def __init__(self, message=None):
        super(OutOfRange, self).__init__(message)


class UnknownVariable(PSExceptionStream):
    def __init__(self, message=None):
        super(UnknownVariable, self).__init__(message)


class InvalidFuncArgs(PSExceptionStream):
    def __init__(self, message=None):
        super(InvalidFuncArgs, self).__init__(message)
