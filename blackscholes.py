from typing import Literal

import numpy as np
from scipy.stats import norm

from put_call_parity import PutCallParity

St = 500
X = 525
q = 0.04
rf = 0.06
vol = 0.15
t = 1 + 7/12

class BlackScholes:
    def __init__(self):
        pass
    
    def calculate_premium(self, options_type:Literal["put", "call"], St:float, X:float, rf:float, q:float, vol:float, T:float):
        d1 = self.d1(St=St, X=X, rf=rf, q=q, vol=vol, T=T)
        d2 = self.d2(d1=d1, vol=vol, T=T)
        
        if options_type == "call":
            return np.exp(-q*T)*St*norm.cdf(d1) - np.exp(-rf*T)*X*norm.cdf(d2)
        elif options_type == "put":
            return np.exp(-rf*T)*X*norm.cdf(-d2) - np.exp(-q*T)*St*norm.cdf(-d1)
    
    def d1(self, St:float, X:float, rf:float, q:float, vol:float, T:float):
        return (np.log(St/X) + (rf-q+0.5*vol**2)*T)/(vol*np.sqrt(T))
    
    def d2(self, d1:float, vol:float, T:float):
        return d1 - vol*np.sqrt(T)
    
if __name__ == "__main__":
    BS = BlackScholes()
    PCP = PutCallParity()
        
    put_price_bt = BS.calculate_premium(options_type="put", St=St, X=X, rf=rf, q=q, vol=vol, T=t)
    print(f"Put premium from bt:", put_price_bt)
    call_price_pcp = PCP.call_premium(P=put_price_bt, S0=St, X=X, rf=rf, q=q, t=t)
    print(f"Call premium from put-call-parity:", call_price_pcp)
    
    call_price_bt = BS.calculate_premium(options_type="call", St=St, X=X, rf=rf, q=q, vol=vol, T=t)
    print(f"Call premium from bt:", call_price_bt)
    put_price_pcp = PCP.put_premium(C=call_price_bt, S0=St, X=X, rf=rf, q=q, t=t)
    print(f"Put premium from put-call-parity:", put_price_pcp)
    
    print("\nDifference in put bt price and pcp price =", put_price_bt - put_price_pcp)
    print("Difference in call bt price and pcp price =", call_price_bt - call_price_pcp)