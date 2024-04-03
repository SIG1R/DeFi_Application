# Martingale
import numpy as np
#from utils import Risk_MEasurement as RM
from scipy.stats import norm
from components.instruments import Option

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

    def func(self, n, p, U, D, type_option):

        summation = 0
        for i in range(n):
            comb = np.math.factorial(n)/ (np.math.factorial(n) * np.math.factorial(n-i))
            pay_off_calc = Option.pay_off(type_option, 
                                self.root*U**(i)*D**(n-i),
                                   8.5)

            summation += comb*p**(i)*(1-p)**(n-i)*pay_off_calc
        return summation


class Black_Scholes:
    
    def __init__(self, option):
        '''
        Inicializate the Black_Scholes instance, for this you need the
        auto reference self and a option instance object.
        '''

        self.option = option

    def pay_off(self, type_option):
        '''
    
        '''

        # >>> Compute D´s <<<
        ln = np.log(self.option.spot/self.option.strike)
        risk_premiun = self.option.risk_free /100

        # Complete risk_premiun by d1
        risk_premiun_d1 = risk_premiun + 0.5 * self.option.volatility**2

        # Complete risk_premiun by d1
        risk_premiun_d2 = risk_premiun - 0.5 * self.option.volatility**2
        
        denominator = self.option.volatility*(4**0.5)

        #if (self.option.interval == 'Semana'):
        #    denominator *= np.sqrt(5)

        #elif (self.option.interval == 'Mes'):
        #    denominator *= np.sqrt(20)

        #else:
        #   denominator *= np.sqrt(250)

    
        self.d1 = (ln + risk_premiun_d1 * self.option.expiration)/denominator
        self.d2 = (ln + risk_premiun_d2 * self.option.expiration)/denominator

        # >>> Compute N(D´s) <<<
        self.prob_d1 = norm.cdf(self.d1)
        self.prob_d2 = norm.cdf(self.d2)

        
        if (type_option == 'Call'):
            self.payoff = self.option.spot*self.prob_d1 - self.option.strike*np.exp(-self.option.risk_free/100*self.option.expiration)*self.prob_d2

        else:
            self.d1 *= -1
            self.d2 *= -1
            self.prob_d1 = norm.cdf(self.d1)
            self.prob_d2 = norm.cdf(self.d2)
            self.payoff =   self.option.strike*np.exp(-self.option.risk_free/100*self.option.expiration)*self.prob_d2 - self.option.spot*self.prob_d1



class Merton(Black_Scholes):
    def __init__(self):
        pass
