# Martingale
import numpy as np
from utils import Risk_MEasurement as RM

class Filtration:
    pass

class Martingale:
    pass

class Binomial_Tree:
    '''
    ¡Only for options!, no bonds, no stocks, only options.
    '''
    
    def __init__(self, S0):
        '''
        '''

        self.root = S0

    def func(n, x, p, U, D):

        summation = 0
        for i in range(n):
            comb = np.math.factorial(i)/ (np.math.factorial(x) * np.math.factorial(i-x))
            summation += comb*p**(x)*(1-p)**(n-x)*self.root*U**(x)*D**(n-x)
        return summation
