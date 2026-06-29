import math
from numbers import Complex, Real
from .vector import Vector

class Comp(Vector, Complex):
    'a complex number. a vector of 2 real numbers'
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag
        super.__init__((real, imag))
    
    @classmethod
    def from_complex(cls, c: Complex) -> Comp:
        return cls(c.real, c.imag)

    def norm(self) -> Real:
        return math.sqrt(self.real * self.real + self.imag * self.imag)
    
    def unit(self) -> Real:
        return type(self)(self.real / self.norm(), self.imag / self.norm())
    
    def conjugate(self) -> Comp:
        return type(self)(self.real, -self.imag)
    
    __abs__ = norm
    
    def __neg__(self) -> Comp:
        return type(self)(-self.real, -self.imag)
    def __pos__(self) -> Comp:
        return type(self)(+self.real, +self.imag)
    
    def __add__(self, other) -> Comp:
        return type(self)(self.real + other.real, self.imag + other.imag)
    
    def __mul__(self, other) -> Comp:
        return type(self)(self.real*other.real-self.imag*other.imag, self.real*other.imag+self.imag*other.real)

    def __complex__(self) -> complex:
        return complex(self.real, self.imag)
            
    def __eq__(self, other) -> bool:
        return self.real == other.real and self.imag == other.imag
                
    # '__pow__',
    # '__radd__',
    # '__rmul__',
    # '__rpow__',
    # '__rtruediv__',
    # '__truediv__',
