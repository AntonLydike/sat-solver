from .logicTree import LogicTreeNode, LogicTreeNode_Atom
from .evaluation import Interpretation, Variables

MAPPINGS = {
    'tex': {
        'separator': '&',
        'line-end': '\\\\'
    },
    'md': {
        '\\lnot': '￢',
        '\\land': '∧',
        '\\lor': '∨',
        '\\to': '→',
        'separator': '|',
        'line-end': ''
    },
    'md-sets': {
        '\\lnot': '\\',
        '\\land': '∪',
        '\\lor': '∩',
        '\\to': '⇒',
        'separator': '|',
        'line-end': ''
    },
    'tex-sets': {
        '\\land': '\\cup',
        '\\lor': '\\cap',
        'separator': '&',
        'line-end': '\\\\'
    }
}


class LogicTable:
    def __init__(self, tree: LogicTreeNode, verbose: bool = False):
        self.tree = tree
        self.inter = Interpretation({})
        self.verbose = verbose

    def getTable(self):
        out = ""

        if (self.verbose):
            trees = list(set(self.tree.nodes()))
            trees.sort(key=lambda x: len(str(x)))
        else:
            trees = [LogicTreeNode_Atom(var) for var in
                     self.tree.getFreeVars()] + [self.tree]

        # generate heading
        out += " & ".join([str(tree) for tree in trees]) + "\\\\ \\hline\n"

        for permutation in Variables.permutations(self.tree.getFreeVars()):
            out += " & ".join([('\\tt' if tree.evaluate(self.inter, permutation) else '\\ff')
                               for tree in trees]) + "\\\\\n"

        print(out)

        return out
