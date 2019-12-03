from functools import reduce
import operator
from .exceptions import IllegalStateException


class LogicTreeNode:
    def __init__(self, action, children):
        self.action = action
        self.children = children

    def evaluate(self, interpretation, variables):
        raise NotImplementedError

    def getFreeVars(self):
        return list(set(filter(None, reduce(operator.concat, [x.getFreeVars() for x in self.children]))))

    def nodes(self):
        return [self] + list(filter(None, reduce(operator.concat, [x.nodes() for x in self.children])))

    def __str__(self):
        children = ", ".join([str(x) for x in self.children])
        return f"{self.action}({children})"

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return self.__str__().__hash__()


class LogicTreeNode_Operator(LogicTreeNode):
    def evaluate(self, inter, var):
        if (self.action == '\\lnot'):
            return not self.children[0].evaluate(inter, var)
        elif(self.action == '\\lor'):
            return self.children[0].evaluate(inter, var) or self.children[1].evaluate(inter, var)
        elif(self.action == '\\land'):
            return self.children[0].evaluate(inter, var) and self.children[1].evaluate(inter, var)
        elif(self.action == '\\to'):
            a = self.children[0].evaluate(inter, var)
            b = self.children[1].evaluate(inter, var)
            return not (a and (not b))

    def __str__(self):
        if (self.action == '\\lnot'):
            return f"{self.action} {str(self.children[0])}"

        return f"{str(self.children[0])} {self.action} {str(self.children[1])}"


class LogicTreeNode_Atom(LogicTreeNode):
    def __init__(self, name):
        super().__init__('variable', [name])

    def evaluate(self, inter, var):
        return var.getValue(self.children[0])

    def getFreeVars(self):
        return self.children

    def nodes(self):
        return [self]

    def __str__(self):
        return self.children[0]


class LogicTreeNode_Predicate(LogicTreeNode):
    def evaluate(self, inter, var):
        return inter.interpret(self.action, self.children)


class LogicTreeNode_Brackets(LogicTreeNode):
    def __init__(self, content):
        super().__init__("brackets", [content])

    def evaluate(self, inter, var):
        if len(self.children) != 1:
            raise IllegalStateException(
                "LogicTreeNode_Brackets expects to have exactly one child node!")
        return self.children[0].evaluate(inter, var)

    def __str__(self):
        return f"({str(self.children[0])})"
