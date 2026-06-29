from numbers import Number
from .vector import Vector

class Octo(Number, Vector):
    'an octonion'
    
    def __init__(self, e0, e1, e2, e3, e4, e5, e6, e7):
        self.e0 = e0
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.e4 = e4
        self.e5 = e5
        self.e6 = e6
        self.e7 = e7

    @classmethod
    def from_complex(cls, c0, c1, c2, c3):
        ...

    @classmethod
    def from_quaternion(cls, q0, q1):
        ...

    def as_real_matrix(self):
        ...

    def as_complex_matrix(self):
        ...
