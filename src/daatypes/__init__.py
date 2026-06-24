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

# an IEEE 754 binary/decimal float
# represents the binary/decimal rationals, plus wierd IEEE 754 arithmetic
from .float import Float 

# a composed datatype
# two arrays of int primes[] and int exponents[]
# represents the rationals 
# conducive to slow additive but fast multiplicative arithmetic
from .monzo import Monzo 

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

# a composed datatype
# an ordered pair of (qint magnitude, float angle)
# represents the complex numbers
# conducive to slow additive but fast multiplicative arithmetic, and uniform angle precision
from .polar import Polar
