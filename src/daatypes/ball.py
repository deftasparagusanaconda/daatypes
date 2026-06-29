from numbers import Number, Real
import daacorations
from dataclasses import dataclass, Field

@dataclass
class Ball(Number):
    'a composed datatype representing an axially symmetric (i think) p-norm ball in an R-vector space'
    
    midpoint: Number
    radius: Real
    power: Real
    
    def __post_init__(self):
        if self.radius < 0:
            raise ValueError(f'{self.radius=} must be non-negative')
        if self.power < 0:
            raise ValueError(f'{self.radius=} must be non-negative')
    
    __repr__ = daacorations.pretty_repr

class EBall:
    'a Ball but with p = 2 (euclidean), thus representing a hypersphere'
