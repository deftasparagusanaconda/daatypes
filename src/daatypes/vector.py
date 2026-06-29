import math
from collections.abc import Sequence, Iterable
from numbers import Real

class Vector(Sequence):
    'an immutable vector'
    def __init__(self, iterable: Iterable):
        self.sequence: tuple = tuple(iterable)
    
    def norm(self, power = 2) -> Real:
        if power == 2: 
            return math.hypot(self.sequence) 
        else: 
            return sum(abs(x) ** power for x in self) ** (1 / power)
    __abs__ = norm
    
    def unit(self): 
        return self / self.norm()
    
    # Sequence interface methods
    def __len__(self):
        return len(self.sequence)
    def __getitem__(self, index):
        return self.sequence[index]

    def __mul__(self, other):
        if isinstance(other, Real):
            return type(self)(x * other for x in self)
    
    def __truediv__(self, other):
        if isinstance(other, Real):
            return type(self)(x / other for x in self)
    
