import math
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


class Node:
    def __init__(self):
        self.state=None
        self.payout=0
        self.ST=0
        self.prob=0

class BinomialTree:
    def __init__(self):
        pass
    
    def calculate_premium(self, options_type:Literal["put", "call"], num_time_steps:int, St:float, X:float, rf:float, q:float, vol:float):
        u = np.exp(vol*np.sqrt(t/num_time_steps))
        d = 1/u

        nodes_list = self.generate_outermost_nodes(options_type=options_type, num_time_steps=num_time_steps, St=St, X=X, u=u, d=d, rf=rf, q=q)
        expected_payout = 0
        prob = 0
        for node in nodes_list:
            # get number of possible pathways to current node
            num_pathways = math.comb(num_time_steps, node.state.count('u'))
            #print("State", node.state, "Payout", node.payout, "Stock Price", node.ST, "Prob", node.prob, "num_pathways", num_pathways)
            
            expected_payout += num_pathways*node.payout*node.prob
            prob += num_pathways*node.prob
            
        #print(prob)
        #print(expected_payout)
            
        options_price = expected_payout*np.exp(-rf*t)
        return options_price
        
    #function to generate probability and payout at outermost nodes of binomial tree to calculate expected payout
    def generate_outermost_nodes(self, options_type:Literal["put", "call"], num_time_steps:int, St:float, X:float, u:float, d:float, rf:float, q:float):
        nodes_list = []
        pu, pd = self.pupd(u=u, d=d, rf=rf, q=q, t=t, num_time_steps=num_time_steps)
        power = num_time_steps
        while power > 0:
            num_of_ud_terms = int((num_time_steps-power)/2)
            #print("num of ud terms", num_of_ud_terms)

            for state_name, state_value, state_prob in [("u",u,pu), ("d",d,pd)]:
                node = Node()
                if num_of_ud_terms != 0:
                    node.state = state_name*power + "ud"*num_of_ud_terms
                else:
                    node.state = state_name*power
                #print(power, state_value)
                node.ST = St*(state_value**power)
                node.prob = (state_prob**power) * ((pu*pd)**(num_of_ud_terms))
                
                if options_type == "put":
                    node.payout = Payout().put_payout(ST=node.ST, X=X)
                elif options_type == "call":
                    node.payout = Payout().call_payout(ST=node.ST, X=X)
                
                nodes_list.append(node)
            
            power -= 2
            
            if power == 0:
                num_of_ud_terms = int((num_time_steps)/2)
                node = Node()
                node.state = "ud"*num_of_ud_terms
                node.ST = St
                if options_type == "put":
                    node.payout = Payout().put_payout(ST=node.ST, X=X)
                elif options_type == "call":
                    node.payout = Payout().call_payout(ST=node.ST, X=X)
                node.prob = (pu*pd)**(num_of_ud_terms)
                nodes_list.append(node)
            
        return nodes_list
    
    # function to generate probability of up pu and probability of down pd
    def pupd(self, u:float, d:float, rf:float, q:float, t:float, num_time_steps:int):
        pu = (np.exp((rf-q)*(t/num_time_steps))-d)/(u-d)
        pd = 1-pu
        #print(pu, pd)
        return pu, pd
    
if __name__ == "__main__":
    BT = BinomialTree()
    PCP = PutCallParity()
    
    for num_time_steps in [100, 500, 1000]:
        print("\nBinomial tree with number of time steps =", num_time_steps)
        
        put_price_bt = BT.calculate_premium("put", num_time_steps=num_time_steps, St=St, X=X, rf=rf, q=q, vol=vol)
        print(f"Put premium from bt:", put_price_bt)
        call_price_pcp = PCP.call_premium(P=put_price_bt, S0=St, X=X, rf=rf, q=q, t=t)
        print(f"Call premium from put-call-parity:", call_price_pcp)
        
        call_price_bt = BT.calculate_premium("call", num_time_steps=num_time_steps, St=St, X=X, rf=rf, q=q, vol=vol)
        print(f"Call premium from bt:", call_price_bt)
        put_price_pcp = PCP.put_premium(C=call_price_bt, S0=St, X=X, rf=rf, q=q, t=t)
        print(f"Put premium from put-call-parity:", put_price_pcp)
        
        print("\nDifference in put bt price and pcp price =", put_price_pcp - put_price_bt)
        print("Difference in call bt price and pcp price =", call_price_pcp - call_price_bt)
    