import math, builtins
from dataclasses import dataclass
from numbers import Number, Rational, Integral
from collections.abc import Sequence, MutableSequence
from typing import Literal
from daacorations import pretty_repr
from fractions import Fraction

@dataclass
class CF(Number):
    'a continued fraction'
    numerators: Sequence
    denominators: Sequence
    signum: Literal[-1, 0, +1] = +1
    numerators_repeat: None | int = None
    denominators_repeat: None | int = None
    
    @property
    def integral(self) -> Integral:
        return self.denominators[0]
    
    @property
    def fractional(self) -> Rational:
        ...

    def __str__(self) -> str:
        sign = {-1: '-', 0: '', +1: '+'}[self.signum]
        return f'{sign}({self.denominators[0]} + {" + ".join(f"{n}/{d}"for n, d in zip(self.numerators[1:], self.denominators[1:]))})'

    __repr__ = pretty_repr

def quotrem_nearest_even(n, d):
    q = round(n / d)
    return q, n - q * d

class SCF(CF, Sequence):
    'a simple continued fraction with a Sequence interface'
    def __init__(self, denominators: Sequence, signum = +1):
        super().__init__([0, 1], denominators, signum, numerators_repeat = 1)
    
    # Sequence methods
    def __getitem__(self, index: int) -> int:
        return self.denominators[index]
    def __len__(self) -> int:
        return len(self.denominators)
    
    @classmethod
    def from_rational(cls, rational: Rational, round = math.floor) -> SCF:
        'set round=builtins.round or round=math.ceil for interesting partial denominators'
        signum = (rational > 0) - (rational < 0)
        rational = abs(rational)
        
        denominators: MutableSequence[int] = list()
        
        while True:
            quotient = round(rational)
            denominators.append(quotient) 
            remainder = rational.numerator - quotient * rational.denominator
            if remainder == 0:
                break
            rational = Fraction(rational.denominator, remainder)
        
        return cls(denominators, signum)
    
    def to_rational(self) -> Rational:
        if len(self.denominators) == 1:
            return self.signum * self.denominators[0]

        ac = Fraction(self.denominators[-1], 1)

        for d in reversed(self.denominators[:-1]):
            ac = d + 1 / ac

        return self.signum * ac

    def __str__(self) -> str:
        return f'[{self.denominators[0]};{",".join(str(d) for d in self.denominators[1:])}]'
    
    __repr__ = pretty_repr
