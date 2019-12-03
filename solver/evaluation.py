class Interpretation:
    def __init__(self, interpretations):
        self.interpretations = interpretations

    def interpret(self, funcname, args):
        if funcname in self.interpretations:
            return self.interpretations[funcname](*args)
        else:
            raise NotImplementedError


class Variables:
    def __init__(self, vars: object = {}):
        self.vars = vars

    def getValue(self, name: str):
        return self.vars[name]

    def setValue(self, name: str, val: bool):
        self.vars[name] = val

    def extend(self, vars):
        return Variables({**self.vars, **vars.vars})

    """
    generates all permutations for a given set of variables
    """
    @staticmethod
    def permutations(variables):
        # we generate the permutations by incrementing a number and then interpreting it as binary
        for perm in range(0, 2 ** len(variables)):
            vars = Variables({})
            # the n-th bit of the number is the state of the n-th variable
            for varnum in range(0, len(variables)):
                vars.setValue(variables[varnum], bool(perm & (1 << varnum)))

            # yield the generated variables
            yield vars
