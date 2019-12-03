import re

from .exceptions import IllegalStateException
from .parserInput import ParserInput
from .logicTree import *

# (p \land \lnot q) \to (r \land s)


def parse_input(input: str):
    input = ParserInput(input)

    try:
        logicTree = ParseState(None).read(input)
    except IllegalStateException as e:
        print(e)
        print(input.getErrMessage())
        raise e

    if not input.isEmpty():
        print("Input parsing terminated early\n" + input.getErrMessage())
        return

    return logicTree


class ParseState:
    def __init__(self, parent):
        self.parent = parent

    def read(self, input: ParserInput, prevRead=None):
        if input.isEmpty():
            if prevRead:
                return prevRead

            raise IllegalStateException("Unexpected end of input!", input)

        # we read an operator
        if input.nextChar() == '\\':
            #print("read operator at \n" + input.getErrMessage())
            return ParseState_Operator(self).read(input, prevRead)

        # we read closing brackets
        if input.nextChar() == ')':
            if prevRead:
                return prevRead
            raise IllegalStateException(
                "Unexpected closing parenthesis", input)

        # only operators support something in front of them
        if prevRead:
            raise IllegalStateException(
                "Operator expected", input)

        if input.nextChar() == '(':
            prevRead = ParseState_Brackets(self).read(input)
            #print("Read brackets at\n" + input.getErrMessage())
            return ParseState(self).read(input, prevRead)

        match = input.matches(r"[A-z]+")

        if not match:
            raise IllegalStateException("Atom expected", input)

        prevRead = LogicTreeNode_Atom(match.group(0))

        #print("read atom at \n" + input.getErrMessage())

        input.consume(match.group(0))

        return ParseState(self).read(input, prevRead)


class ParseState_Operator(ParseState):
    def read(self, input: ParserInput, prevRead=None):

        if input.startswith('\\lnot'):
            if prevRead != None:
                raise IllegalStateException(
                    "\\lnot only takes one argument", input)

            input.consume('\\lnot')
            return LogicTreeNode_Operator("\\lnot", [super().read(input)])

        match = input.matches(r"\\(lor|land|to)")

        if match:
            operator = match.group(0)

            if prevRead == None:
                raise IllegalStateException(
                    operator + " is missing the first argument", input)

            # remove read part from input string
            input.consume(operator)
            return LogicTreeNode_Operator(operator, [prevRead, super().read(input)])
        else:
            raise IllegalStateException("Unknown operator", input)


class ParseState_Brackets(ParseState):
    def read(self, input: ParserInput, prevRead=None):
        # remove opening brackets
        input.consume(1)

        # fail if we have a previous node (e.g. "b (a \lor b)" is an invalid input)
        if prevRead:
            raise IllegalStateException(
                "Parenthesis cannot be preceeded by an expression", input)

        if input.nextChar() == ")":
            raise IllegalStateException("Empty parenthesis", input)

        # read next node
        logicNode = LogicTreeNode_Brackets(super().read(input))

        if input.nextChar() != ')':
            raise IllegalStateException("Closing parenthesis expected", input)

        # consume closing parenthesis
        input.consume(1)
        return logicNode
