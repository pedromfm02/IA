class BayesNet:

    def __init__(self, ldep=None):  # Why not ldep={}? See footnote 1.
        if not ldep:
            ldep = {}
        self.dependencies = ldep

    # The network data is stored in a dictionary that
    # associates the dependencies to each variable:
    # { v1:deps1, v2:deps2, ... }
    # These dependencies are themselves given
    # by another dictionary that associates conditional
    # probabilities to conjunctions of mother variables:
    # { mothers1:cp1, mothers2:cp2, ... }
    # The conjunctions are frozensets of pairs (mothervar,boolvalue)
    def add(self,var,mothers,prob):
        self.dependencies.setdefault(var,{})[frozenset(mothers)] = prob

    # Joint probability for a given conjunction of
    # all variables of the network
    def jointProb(self,conjunction):
        prob = 1.0
        for (var,val) in conjunction:
            for (mothers,p) in self.dependencies[var].items():
                if mothers.issubset(conjunction):
                    prob*=(p if val else 1-p)
        return prob
    
    def individualProb(self, variable, value):
        conjs = self._gen_conjunctions(
            [v for v in self.dependencies.keys() if v != variable]
        )
        return sum(
            [self.jointProb([(variable, value)] + c) for c in conjs]
        )

    def _gen_conjunctions(self, variables):
        if len(variables) == 1:
            return [
                [(variables[0], True)],
                [(variables[0], False)],
            ]
        res = []
        for c in self._gen_conjunctions(variables[1:]):
            res.append([(variables[0], True)] + c)
            res.append([(variables[0], False)] + c)
        return res
    
# Footnote 1:
# Default arguments are evaluated on function definition,
# not on function evaluation.
# This creates surprising behaviour when the default argument is mutable.
# See:
# http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments

