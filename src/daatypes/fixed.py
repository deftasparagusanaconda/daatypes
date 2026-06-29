from stringman.unicode import to_subscript
from numbers import Rational, Integral
from collections.abc import Sequence, MutableSequence, Iterable
from typing import Literal
from dataclasses import dataclass, field
from itertools import chain, cycle, repeat
import math

@dataclass(kw_only = True)
class Fixed(Rational):
    'a rational number with a fixed radix point. could potentially be an n-adic number class some day…'
    signum: Literal[-1, 0, +1]
    radix: Integral
    left: Sequence[Integral] = field(default_factory = tuple)
    right: Sequence[Integral] = field(default_factory = tuple)
    left_repeat: None | Integral = None
    right_repeat: None | Integral = None

    def to_fraction(self) -> Fraction:
        value = self.signum * sum(chain(
            (digit * self.radix ** i for i, digit in enumerate(self.left, start = 0)),
            (digit * self.radix ** -i for i, digit in enumerate(self.right, start = 1))))

    @property
    def numerator(self) -> Integral:
        if self.left_repeat is not None:
            raise ValueError(f'{self} is not a rational number')
        return 
    @property
    def denominator(self) -> Integral:
        if self.left_repeat is not None:
            raise ValueError(f'{self} is not a rational number')
        return 
                    
    @property
    def left_preperiod(self):
        return self.left if self.left_repeat is None else self.left[:self.left_repeat]
    @property
    def right_preperiod(self):
        return self.right if self.right_repeat is None else self.right[:self.right_repeat]
    @property
    def left_repetend(self):
        return () if self.left_repeat is None else self.left[self.left_repeat:]
    @property
    def right_repetend(self):
        return () if self.right_repeat is None else self.right[self.right_repeat:]
    @property
    def left_iterable(self) -> Iterable:
        yield from self.left_preperiod
        if self.left_repetend: 
            yield from cycle(self.left_repetend) 
        else: 
            yield from repeat(0)
    @property
    def right_iterable(self) -> Iterable:
        yield from self.right_preperiod
        if self.right_repetend: 
            yield from cycle(self.right_repetend) 
        else: 
            yield from repeat(0)
    
    @classmethod
    def from_integral(cls, integral: Integral, radix: Integral) -> Fixed:
        if integral == 0:
            return cls(signum=0, radix=radix)
        signum = (integral > 0) - (integral < 0)
        integral = abs(integral)
        
        left: MutableSequence[Integral] = list()
        while integral > 0:
            integral, index = divmod(integral, radix)
            left.append(index)
        
        return cls(signum=signum, left=left, radix=radix)
    
    @classmethod
    def from_rational(cls, rational: Rational, radix: Integral, right_limit: None | int = None) -> Fixed:
        if rational == 0:
            return cls(signum=0, radix=radix)
        
        signum = (rational > 0) - (rational < 0)
        rational = abs(rational)
        
        integral, remainder = divmod(rational.numerator, rational.denominator)

        left: MutableSequence[Integral] = list()
        while integral > 0:
            integral, index = divmod(integral, radix)
            left.append(index)
        
        right: MutableSequence = list()
        remainders: dict[int, int] = dict() # remainders[remainder] = index
        
        while True:
            if remainder == 0 or remainder in remainders:
                break 
            
            remainders[remainder] = len(right)
            
            digit, remainder = divmod(remainder * radix, rational.denominator)
            right.append(digit)

            if right_limit is not None and len(right) >= right_limit:
                break
        
        return cls(signum = signum, radix = radix, left=left, right=right, right_repeat = remainders.get(remainder, None))
    
    def __pos__(self) -> Fixed:
        return self
    def __neg__(self) -> Fixed:
        return type(self)(signum=-self.signum, radix=self.radix, left=left, right=right, left_repeat=left_repeat, right_repeat=right_repeat)
    def __abs__(self) -> Fixed:
        return type(self)(signum=+1, radix=self.radix, left=left, right=right, left_repeat=left_repeat, right_repeat=right_repeat)
    def __add__(self, other) -> Fixed:
        ...
    def __floor__(self) -> Fixed:
        return type(self)(signum=self.signum, radix=self.radix, left=left, right=right, left_repeat=left_repeat, right_repeat=right_repeat)
    def __ceil__(self) -> Fixed:
        return 
    def __trunc__(self) -> Fixed:
        return type(self)(signum=self.signum, radix=self.radix, left=left, left_repeat=left_repeat)
    def __floordiv__(self, other) -> Fixed:
        return 
    def __le__(self, other) -> bool:
        return 
    def __lt__(self, other) -> bool:
        return self <= other and not other <= self
    def __mod__(self, other) -> Fixed:
        return 
    def __mul__(self, other) -> Fixed:
        return 
    def __pow__(self, other) -> Fixed:
        return 
    def __radd__(self) -> Fixed:
        return 
    def __rfloordiv__(self) -> Fixed:
        return 
    def __rmod__(self) -> Fixed:
        return 
    def __rmul__(self) -> Fixed:
        return 
    def __round__(self) -> Fixed:
        return 
    def __rpow__(self) -> Fixed:
        return 
    def __rtruediv__(self) -> Fixed:
        return 
    def __truediv__(self) -> Fixed:
        return 
    
    def __float__(self) -> float:
        if self.left_repeat is not None:
            return self.signum * math.inf
        return self.signum * sum(chain(
            (digit * self.radix ** i for i, digit in enumerate(self.left, start = 0)),
            (digit * self.radix ** -i for i, digit in enumerate(self.right, start = 1))))

    def __str__(self, char_set = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') -> str:
        return ''.join(chain(
            {-1: '−', 0: '', +1: '+'}[self.signum],
            '(',
            (char_set[digit] for digit in reversed(self.left_repetend)) if self.left_repeat is not None else '0',
            ')',
            (char_set[digit] for digit in reversed(self.left_preperiod)),
            '.',
            (char_set[digit] for digit in self.right_preperiod),
            '(',
            (char_set[digit] for digit in self.right_repetend) if self.right_repeat is not None else '0',
            ')',
            to_subscript(str(self.radix))))

def round_expansion(integral, fractional, radix, tie):
    'round a positional number'
    twice = 2 * remainder

    if twice < divisor:
        # round down/do nothing
        return integral, fractional_digits, None
    elif twice == divisor:
        # a tie. like rounding 0.95 to 1 decimal digit. you have to choose a rule
        match tie:
            case 'up': fractional_digits[-1] += 1
            case 'down': fractional_digits[-1] += 0
            case 'even': fractional_digits[-1] += fractional_digits[-1] % 2 == 1
            case 'odd': fractional_digits[-1] += fractional_digits[-1] % 2 == 0
    elif twice > divisor:
        fractional_digits[-1] += 1
    
    # propagate the addition
    for i in range(fractional_digit_count - 1, 0, -1):
        if fractional_digits[i] >= radix:
            fractional_digits[i] = 0
            fractional_digits[i - 1] += 1
    if fractional_digits[0] >= radix:
        integral += 1
''' 
def rational_to_scientific(rational: Rational, precision: int, radix: int = 10, exponent_marker: str = 'e', char_set: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') -> str:
    'stringify a rational number to scientific format (e.g. 1/3 → +3.(3)e-1)'
    
    if rational == 0:
        return '0' + exponent_marker + '0'

    # normalize significand and exponent so that 1 <= significand < radix
    sig: Rational = abs(rational)
    exp: int = 0
    while not 1 <= sig:
        sig *= radix
        exp -= 1
    while not sig < radix:
        sig /= radix
        exp += 1

    # now we just need to convert sig rational to digits, and exponent integer to digits
    sig_sign = '' if rational == 0 else ('-' if rational < 0 else '+').lstrip('+')
    sig = rational_to_digits(sig, fractional_precision = precision - 1, radix = radix, char_set = char_set)
    exp_sign = '' if exp == 0 else ('-' if exp < 0 else '+')
    exp = integral_to_digits(exp, radix = radix, char_set = char_set).lstrip('+')
    
    return sig_sign + sig + exponent_marker + exp_sign + exp
'''
