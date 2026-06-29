import math
from numbers import Number, Real, Complex
from dataclasses import dataclass
from daacorations import pretty_repr

@dataclass
class Quat(Number):
    'a quaternion. a vector of 4 real numbers with special multiplication rules'
    
    w: Real
    x: Real
    y: Real
    z: Real
    
    # @property
    # def real(self) -> float:
    #     return self.w
    #
    # @property
    # def imag(self) -> tuple[float, float, float]:
    #     return self.x, self.y, self.z
    
    def norm(self) -> Real:
        #return math.hypot(self.w, self.x, self.y, self.z)
        return math.sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)
    __abs__ = norm

    def unit(self) -> Real:
        norm = self.norm()
        return type(self)(self.w/norm, self.x/norm, self.y/norm, self.z/norm)

    @classmethod
    def from_complex(cls, a: Complex, b: Complex) -> Quat:
        'construct a quaternion from a pair of complex numbers, by cayley dickson construction'
        return cls(a.real, a.imag, b.real, b.imag)
    
    __repr__ = pretty_repr
    
    def __add__(self, other) -> Quat:
        return type(self)(self.w + other.w, self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other) -> Quat:
        return type(self)(self.w - other.w, self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other) -> Quat:
        return 
    
    def __str__(self) -> str:
        return f'({self.w} + {self.x}i + {self.y}j + {self.z}k)'
    
    def as_real_matrix(self):
        return (( self.w, -self.x, -self.y, -self.z), 
                ( self.x,  self.w, -self.z,  self.y), 
                ( self.y,  self.z,  self.w, -self.x), 
                ( self.z, -self.y,  self.x,  self.w))
    
    def as_complex_matrix(self):
        return ((complex( self.w, self.x), complex(self.y,  self.z)),
                (complex(-self.y, self.z), complex(self.w, -self.x)))
    
