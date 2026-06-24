from numbers import Number
import daacorations

class Ball(Number):
    'a composed datatype representing'
    def __init__(self, midpoint, radius):
        self.midpoint = midpoint
        self.radius = radius
    
    __repr__ = daacorations.pretty_repr
