from .parserInput import ParserInput


class IllegalStateException(Exception):
    def __init__(self, message: str, input: ParserInput = None):
        if (input == None):
            super().__init__(self, message)
        else:
            super().__init__(self, message + " at \n" + input.getErrMessage())
