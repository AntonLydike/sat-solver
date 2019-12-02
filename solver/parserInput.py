import re


class ParserInput:
    def __init__(self, input: str):
        self.pos = 0
        self.input = input
        self.__len = len(input)

    def startswith(self, prefix: str):
        return self.input.startswith(prefix, self.pos)

    def consume(self, count: int):
        if type(count) == str:
            count = len(count)

        self.pos += count
        self.trim()

    def len(self):
        return self.__len - self.pos

    def trim(self):
        while(self.pos < self.__len and self.input[self.pos] == ' '):
            self.pos += 1

    def isEmpty(self):
        return self.pos >= self.__len

    def matches(self, regex: str):
        return re.search(regex, self.input[self.pos:])

    def getErrMessage(self):
        return self.input + "\n" + (" " * self.pos) + "^"

    def string(self):
        return self.input[self.pos:]

    def nextChar(self):
        return self.input[self.pos:self.pos+1]
