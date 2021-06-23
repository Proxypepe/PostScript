def IndexTrace(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Invalid syntax"
    return wrapper


def VarTrace(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Invalid var"
    return wrapper


class InvalidBars(Exception):
    """Invalid number of braces
    """
    def __init__(self, index=0):
        self.index_of_error = index

    def __str__(self):
        if self.index_of_error == 0:
            return f"Invalid number of braces"
        return f"Invalid number of braces {self.index_of_error}"
