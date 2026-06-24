from numbers import Complex

class Polar(Complex):
    def __init__(self, magnitude: Rational, angle: Rational):
        self.magnitude: Rational = magnitude
        self.angle: Rational = angle
