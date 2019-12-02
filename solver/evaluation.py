class Interpretation:
    def __init__(self, interpretations):
        self.interpretations = interpretations

    def interpret(self, funcname, args):
        if funcname in self.interpretations:
            return self.interpretations[funcname](*args)
        else:
            raise NotImplementedError


class Variables:
    def __init__(self, vars):
        self.vars = vars

    def getValue(self, name):
        return self.vars[name]
