import numpy as np


class PutCallParity():
    def __init__(self):
        pass
    
    def call_premium(self, P:float, S0:float, X:float, rf:float, q:float, t:float):
        """
        P: Put premium
        """
        return self.portfolio_b_cost(S0=S0, X=X, rf=rf, q=q, t=t) + P
    
    def put_premium(self, C:float, S0:float, X:float, rf:float, q:float, t:float):
        """
        C: call premium
        """
        return C - self.portfolio_b_cost(S0=S0, X=X, rf=rf, q=q, t=t)
    
    def portfolio_b_cost(self, S0:float, X:float, rf:float, q:float, t:float):
        return S0*np.exp(-q*t) - X*np.exp(-rf*t)