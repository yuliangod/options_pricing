from typing import Literal

import numpy as np

from payout import Payout
from put_call_parity import PutCallParity

St = 500
X = 525
q = 0.04
rf = 0.06
vol = 0.15
t = 1 + 7/12

np.random.seed(40)

class MonteCarlo:
    def __init__(self):
        pass
    
    def simulate(self, options_type:Literal["put", "call"], n:int, St:float, X:float, t:float, rf:float, q:float, vol:float):
        """
        n: number of iterations to run simulation
        """
        
        payout_list = []
        for _ in range(n):
            ST = St*np.exp(self.sampled_return(t=t, rf=rf, q=q, vol=vol))
            if options_type == "put":
                payout = Payout().put_payout(ST=ST, X=X)
            elif options_type == "call":
                payout = Payout().call_payout(ST=ST, X=X)
            payout_list.append(payout)
            
        expected_payout = sum(payout_list)/len(payout_list)
        options_price = expected_payout*np.exp(-rf*t)
        return options_price
    
    # get returns from 1 sample
    def sampled_return(self, t:float, rf:float, q:float, vol:float):
        """
        t: expiration date T in terms of years
        rf: annualised risk-free rate (continuosly compounded)
        q: annualised divided rate
        vol: annualised volatility of returns
        """
        sample_mean = (rf - q - 0.5*vol**2)*t
        sample_var = vol**2*t
        return np.random.normal(loc=sample_mean, scale=np.sqrt(sample_var))

if __name__ == "__main__":
    MC = MonteCarlo()
    PCP = PutCallParity()
    
    for n in [1000, 10000, 100000]:
        print("\nSimulation with n =", n)
        
        put_price_mc = MC.simulate(options_type="put", n=n, St=St, X=X, t=t, rf=rf, q=q, vol=vol)
        print(f"Put premium from simulation:", put_price_mc)
        call_price_pcp = PCP.call_premium(P=put_price_mc, S0=St, X=X, rf=rf, q=q, t=t)
        print(f"Call premium from put-call-parity:", call_price_pcp)
        
        call_price_mc = MC.simulate(options_type="call", n=n, St=St, X=X, t=t, rf=rf, q=q, vol=vol)
        print(f"Call premium from simulation:", call_price_mc)
        put_price_pcp = PCP.put_premium(C=call_price_mc, S0=St, X=X, rf=rf, q=q, t=t)
        print(f"Put premium from put-call-parity:", put_price_pcp)
        
        print("\nDifference in put simu price and pcp price =", put_price_mc - put_price_pcp)
        print("Difference in call simu price and pcp price =", call_price_mc - call_price_pcp)
    