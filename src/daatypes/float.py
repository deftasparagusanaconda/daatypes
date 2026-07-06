import daacorations, math, builtins
from numbers import Rational
from fractions import Fraction
from dataclasses import dataclass
def xor(a, b): return (a and b) or (not(a or b))

def fraction_to_radix(numerator: int, denominator: int, *, 
            radix: int,
            alphabet: str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            fractional_digit_count: int = 99) -> str:

    print(radix, numerator, denominator)

    assert isinstance(numerator, int)
    assert isinstance(denominator, int)

    positive = xor(numerator >= 0, denominator >= 0)
    sign = '' if positive else '-'
    
    integral, fractional = divmod(abs(numerator), abs(denominator))
    
    if integral == 0:
        integral_str = '0'
    else:
        integral_digits: list[str] = []
        while integral:
            integral_digits.append(alphabet[integral % radix])
            integral //= radix
        integral_str = ''.join(reversed(integral_digits))

    if fractional == 0:
        return sign + integral_str

    seen: dict[int, int] = dict()
    fractional_digits: list[str] = list()

    for _ in range(fractional_digit_count):
        if not fractional:
            break

        if fractional in seen:
            # repeating pattern
            index = seen[fractional]
            return sign + integral_str + '.' + ''.join(fractional_digits[:index]) + '(' + ''.join(fractional_digits[index:]) + ')'

        seen[fractional] = len(fractional_digits)
        
        fractional *= radix
        digit = fractional // denominator
        fractional %= denominator
        fractional_digits.append(alphabet[digit])
    else:
        return sign + integral_str + '.' + ''.join(fractional_digits) + '…'
    
    return sign + integral_str + '.' + ''.join(fractional_digits)

@dataclass(kw_only = True)
class Float(Rational):
    """store a rational number in scientific notation as a floating-point number

    example
    -------
    significand * radix ** (exponent - precision + 1)
    S.SSSSSS * RR ^ (EE - P + 1)
    1.234567 * 10 ^ (89 - 7 + 1)

    notes to myself
    ---------------
    when printing to another radix, if input radix and output radix are coprime, you need to specify precision to the equivalent of the input radix. 
    """
    significand: int
    precision: int
    radix: int
    exponent: int

    @property
    def numerator(self) -> int:
        return self.significand * self.radix ** max(0, self.exponent - self.precision + 1)
    
    @property
    def denominator(self) -> int:
        return self.radix ** max(0, self.precision - 1 - self.exponent)
    
    @classmethod
    def from_str(cls, string: str, *, radix: int = 10, precision: None | int = None, exponent_marker: str = 'e') -> Float:
        'construct a Float from a string. radix=10 by default (like builtins.int). precision is inferred.'
        # '-0,1.2,3E-4,5'
        string = string.replace(',', '').lower()
        # '-01.23e-45'
        significand_str, exponent_str = string.split(exponent_marker, 1) if exponent_marker in string else (string, '0')
        # '-01.23', '-45'
        negative = significand_str.startswith('-')
        digits = significand_str.lstrip('+-0')
        # -ve, '1.23', '-45'
        point = digits.find('.') if '.' in digits else len(digits)
        digits = digits.replace('.', '')
        # -ve, '123', point=1, '-45'
        
        precision = len(digits) if precision is None else precision
        significand = int(('-' if negative else '') + digits, base=radix)
        exponent = int(exponent_str, base=radix) + point - 1
        
        return cls(radix=radix, precision=precision, significand=significand, exponent=exponent)
    
    @classmethod
    def from_rational(cls, rational: Rational, *, radix: int, precision: int) -> Float:
        signum = (rational > 0) - (rational < 0)

        significand = abs(rational)
        exponent = 0

        # get exponent
        while significand >= radix:
            exponent += 1
            significand /= radix
        
        # get significand
        
        significand = Fixed.from_rational(significand)
        
        return cls(radix=radix, precision=precision, significand=significand, exponent=exponent)
    
    def __pos__(self): return Float.from_rational(+Fraction(self))
    def __neg__(self): return Float.from_rational(-Fraction(self))
    def __abs__(self): return Float.from_rational(abs(Fraction(self)))
    def __ceil__(self): return Float.from_rational(math.ceil(Fraction(self)))
    def __floor__(self): return Float.from_rational(math.floor(Fraction(self)))
    def __round__(self): return Float.from_rational(round(Fraction(self)))
    def __trunc__(self): return Float.from_rational(math.trunc(Fraction(self)))
    def __floordiv__(self, other): return Float.from_rational(Fraction(self) // Fraction(other))
    def __mod__(self, other): return Float.from_rational(Fraction(self) % Fraction(other))
    def __le__(self, other): return Fraction(self) <= Fraction(other)
    def __lt__(self, other): return Fraction(self) < Fraction(other)
    def __add__(self, other): return Float.from_rational(Fraction(self) + Fraction(other))
    def __mul__(self, other): return Float.from_rational(Fraction(self) * Fraction(other))
    def __truediv__(self, other): return Float.from_rational(Fraction(self) / Fraction(other))
    def __pow__(self, other): return Float.from_rational(Fraction(self) ** Fraction(other))
    def __rfloordiv__(other, self): return Float.from_rational(Fraction(self) // Fraction(other))
    def __radd__(other, self): return Float.from_rational(Fraction(self) + Fraction(other))
    def __rmul__(other, self): return Float.from_rational(Fraction(self) * Fraction(other))
    def __rmod__(other, self): return Float.from_rational(Fraction(self) % Fraction(other))
    def __rpow__(other, self): return Float.from_rational(Fraction(self) ** Fraction(other))
    def __rtruediv__(other, self): return Float.from_rational(Fraction(self) / Fraction(other))

    def as_fraction(self) -> Fraction:
        return Fraction(self)

    def __float__(self) -> builtins.float:
        return builtins.float(self.as_fraction())

    def __str__(self, *, radix: int = 10, exponent_marker: str = 'e') -> str:
        return f'{self.significand} * {self.radix} ** {self.exponent}'
    
    __repr__ = daacorations.pretty_repr

def ieee_binary(bits: int) -> type:
    match bits: 
        case 16: precision = 11; emin = -  14; emax =   15
        case 32: precision = 24; emin = - 126; emax =  127
        case 64: precision = 53; emin = -1022; emax = 1023
        case  _:
            if bits < 128 or bits % 32 != 0:
                raise ValueError('IEEE defines interchange formats for bits: 16, 32, 64, and multiples of 32 ≥128')
        
            exponent_digits = round(4 * math.log2(bits)) - 13
            precision = bits - exponent_digits
            emax = 2 ** (exponent_digits - 1) - 1
            emin = 1 - emax

    class IEEE754Binary(Float):
        'an IEEE 754 binary float'
    
        def __init__(self, significand: int, exponent: int):
            super().__init__(radix=2, precision=precision, significand=significand, exponent=exponent)

        @classmethod
        def from_str(cls, string) -> IEEE754Binary:
            return super().from_str(string, radix = 2, precision = precision)
    
    return IEEE754Binary, emin, emax

def ieee_decimal(bits: int) -> type:
    match bits:
        case 32: precision =  7; emin = - 95; emax =  96
        case 64: precision = 16; emin = -383; emax = 384
        case  _:
            if bits < 128 or bits % 32 != 0:
                raise ValueError('IEEE defines interchange formats for bits: 32, 64, and multiples of 32 ≥128')
            
            precision = 9 * (bits // 32) - 2
            emax = 3 * 2 ** ((2 * (bits // 32) + 4) - 1)
            emin = 1 - emax

    class IEEE754Decimal(Float):
        'an IEEE 754 decimal float'
    
        def __init__(self, significand: int, exponent: int):
            super().__init__(radix=10, precision=precision, significand=significand, exponent=exponent)
        
        @classmethod
        def from_str(cls, string, *, radix = 10) -> IEEE754Decimal:
            return super().from_str(string, radix = radix, precision = precision)
        
    return IEEE754Decimal, emin, emax

f16  = ieee_binary( 16)
f32  = ieee_binary( 32)
f64  = ieee_binary( 64)
f128 = ieee_binary(128)
f256 = ieee_binary(256)

d32  = ieee_decimal( 32)
d64  = ieee_decimal( 64)
d128 = ieee_decimal(128)


'''
f16:
0 00000 0000000000
False/True 00001–11110 0000000000
−/+ [−14, +15] [0/2E10, 1023/2E10]

d32:
0 000 0000000
−/+ −95, +96] [0/1E7, 9999999/1E7]
'''
