import numbers
from dataclasses import dataclass

@dataclass
class Real(numbers.Real):
    value: Real
    
    def norm(self) -> Real:
        return abs(self.value)
    
    def unit(self) -> Real:
        return (self.value > 0) - (self.value < 0)
    
    
    
    
