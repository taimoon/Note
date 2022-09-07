from math import gcd
class Rational:
    def __init__(self, n, d):
        assert(d != 0) # rational cannot have zero denominator
        common_divisor = gcd(n,d)
        self.numer = n // common_divisor
        self.denom = d // common_divisor
        
    def __add__(self, other):
        return Rational(self.numer*other.denom + self.denom*other.numer, 
                        self.denom*other.denom)
    
    def __repr__(self) -> str:
        return f"Rational({self.numer},{self.denom})"