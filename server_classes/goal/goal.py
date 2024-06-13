from __future__ import annotations

class Goal:
    def __init__(self,weight:int=1,regression:float=1):
        self.weight:int=weight
        self._change_probability:float=1.0
        self._regression:float=regression
    
    @property
    def change_probability(self)->float:
        return self._change_probability
    
    @change_probability.setter
    def change_probability(self, probability:float)->float:
        self._change_probability=probability
        
    def regression(self)->None:
        if self._change_probability>0:
            self._change_probability-=self._regression
        else:
            self._change_probability=0
        
    def __repr__(self)->str:
        return f"Goal(Weight={self.weight}, Regression={self._regression}, Probability={self.change_probability})"
    
    def __str__(self)->str:
        return f"Weight: {self.weight}, Regression: {self._regression}, Probability: {self.change_probability}"