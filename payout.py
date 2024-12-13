import numpy as np


class Payout():
    def put_payout(self, ST:float, X:float):
        """
        ST: stock price at expiration
        X: strike price
        """
        return max(X-ST, 0)
    
    
    def call_payout(self, ST:float, X:float):
        """
        ST: stock price at expiration
        X: strike price
        """
        return max(ST-X, 0)
    