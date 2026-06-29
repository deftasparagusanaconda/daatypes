from numbers import Complex, Rational
from dataclasses import dataclass

@dataclass
class Polar(Complex):
    magnitude: Rational
    angle: Rational

    

