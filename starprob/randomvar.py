import prob_utils as util
from math import * 

class BaseRV:
    
    def __init__(self, *args, **kwargs):
        pass

    def expectation(self):
        util.raiseUndefined()

    def variance(self):
        util.raiseUndefined()

    def sd(self):
        util.raiseUndefined()

class MultinomRV:
    """
    chs = [
        {"p": 0.5, "alias": "good"},
        {"p": 0.3, "alias": "bad"}
    ]

    m = MultinomRV(choices = chs)

    or 

    pbs = [0.1, 0.2, 0.5]
    val = [1, 4, 7]
    alias = ["r", "g", "b"]

    m = MultinomRV(pbs, val)

    """

    def __init__(self, pbs = None, val = None, alias = [], **args):

        self.choices = []

        if pbs:
            util.raiseIfNotAllNumeric(pbs)
            if not val:
                val = range(1, len(pbs) + 1)
            else:
                util.raiseIfNotAllNumeric(val)
            if len(val) is not len(pbs):
                raise ValueError("*** number of values must match number of probs")
        else:
            if "choices" not in args:
                util.raiseMissingArgument("choices")
            choices = args["choices"]

            pbs, val, alias = [], [], []
            self.valFlag = False
            for i, chs in enumerate(choices):
                pbs.append(chs["p"])
                if "val" in chs:
                    val.append(chs[val])
                    self.valFlag = True
                elif self.valFlag:
                    raise ValueError("***`val` need to be consistently specified in `choices`")
                else:
                    val.append(i)
                alias.append(chs["alias"] if "alias" in chs else None)

            if self.valFlag:
                util.raiseIfNotAllNumeric(val)
            util.raiseIfNotAllNumeric(pbs)

        psum = sum(pbs)
        if psum != 1:
            print("=> sum of probability not equal to 1, normalization will be applied")
        factor = 1 / psum

        culProb = 0

        for i in range(len(pbs)):
            normP = pbs[i] * factor
            culProb = culProb + normP
            # each choice is a (value, alias) tuple
            tag = alias[i] if i < len(alias) else None
            self.choices.append( (culProb, normP, val[i], tag) )
    
    def rand(n = 1):
        
    
    def expectation(self):
        if not self.valFlag:
            print("=> Values not given in constructor. Auto-generated values may have no meaning")
        return sum(map(lambda a: a[1] * a[2], self.choices))

    def secondMom(self):
        return sum(map(lambda a: a[1] * a[2] ** 2, self.choices))
    
    def variance(self):
        return self.secondMom() - self.expectation() ** 2
    
    def sd(self):
        return sqrt(self.variance())



        
