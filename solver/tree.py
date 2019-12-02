from .exceptions import IllegalStateException


class LogicTreeNode:
    def __init__(self, action, children):
        self.action = action
        self.children = children

    def evaluate(self, interpretation, variables):
        raise NotImplementedError


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


class LogicTreeNode_Atom(LogicTreeNode):
    def __init__(self, name):
        super().__init__('variable', [name])

    def evaluate(self, inter, var):
        return var.getValue(self.children[0])


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
