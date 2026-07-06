# hello! welcome to daatypes where i propose my own datatypes i find useful in my work

# unsigned integer
# represents the natural numbers starting from zero
# can also do saturating and modular arithmetic
from .uint import UInt 

# 2's complement signed integer
# represents the integers
# can also do saturating and modular arithmetic
from .int import Int 

# unsigned binary fixed point number format
# represents the non-negative binary rationals
# can also do saturating and modular arithmetic
from .uqint import UQInt

# signed binary fixed point number format
# represents the binary rationals
# can also do saturating and modular arithmetic
from .qint import QInt 

# fixed point numbers
from .fixed import Fixed

# scientific notation in arbitrary radix
# represents the rational numbers
from .float import Float, ieee_binary, ieee_decimal, f16, f32, f64, f128, f256, d32, d64, d128

# a composed datatype
# two arrays of int primes[] and int exponents[]
# represents the rationals 
# conducive to slow additive but fast multiplicative arithmetic
from .monzo import Monzo 

# (simple)? continued fraction
from .cf import CF, SCF

# a composed datatype
# an ordered pair of (any lower, any upper)
# represents a closed-closed interval on the real number line
# conducive to fast tolerance-aware arithmetic
from .interval import Interval 

# a composed datatype
# an ordered pair of (centre, +ve radius)
# represents a ball in an R-vector space
# conducive to tolerance-aware arithmetic with accurate tolerance
from .ball import Ball 

# vectors of real numbers ------------------------------------------------------

from .vector import Vector

# represents the real numbers
from .real import Real

# a composed datatype
# represents the complexes in cartesian form
from .comp import Comp

# a composed datatype
# represents the quaternions in cartesian form
from .quat import Quat

# a composed datatype
# represents the quaternions in cartesian form
from .octo import Octo

# a composed datatype
# an ordered pair of (qint magnitude, float angle) where angle is from real axis to imaginary axis
# represents the complex numbers
# conducive to slow additive but fast multiplicative arithmetic, and uniform angle precision
from .polar import Polar

# optimization -----------------------------------------------------------------

from .pareto_front import ParetoFront
