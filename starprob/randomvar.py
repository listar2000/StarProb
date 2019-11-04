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

class MultinomRV(BaseRV):
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

class ExponentialRV(BaseRV):
    """
    Discription:
    A continuous random variable that follows exponential distribution, which is the 
    time between successive arrival (event) in a Poisson arrival process.

    Connections:
    1. The summation of multiple independent exponential random varibles creates a gamma 
    random variable.
    2. Let c be a constant, and X a standard exponential random variable (lambda = 1), 
    then cX follows a exponential distribution with lambda = 1/c
    """

    # class methods 
    def __init__(self, lambd = 1):
        if lambd <= 0:
            raise util.raiseIllValue("lambda <= 0", True)
        self.lambd = lambd
    
    def expectation(self):
        return ExponentialRV.get_exp(self.lambd)
    
    def variance(self):
        return ExponentialRV.get_var(self.lambd)
    
    def sample(self):
        pass

    # static methods
    @staticmethod
    def get_exp(lambd):
        if not lambd:
            util.raiseMissingArgument("lambd")
            return None
        return 1 / lambd
    
    @staticmethod
    def get_var(lambd):
        return 1 / lambd ** 2









        
