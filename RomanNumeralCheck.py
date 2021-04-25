'''
Created on Feb 7, 2013

https://stackoverflow.com/questions/20973546/check-if-an-input-is-a-valid-roman-numeral/20973639#20973639

@author: olegs
'''

ROMAN_CONSTANTS = (
            ( "", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX" ),
            ( "", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC" ),
            ( "", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM" ),
            ( "", "M", "MM", "MMM", "",   "",  "-",  "",    "",     ""   ),
        )

ROMAN_SYMBOL_MAP = dict(I=1, V=5, X=10, L=50, C=100, D=500, M=1000)

CUTOFF = 4000
BIG_DEC = 2900
BIG_ROMAN = "MMCM"
ROMAN_NOUGHT = "nulla"

def digits(num):
    if num < 0:
        raise Exception('range error: negative numbers not supported')
    if num % 1 != 0.0:
        raise Exception('floating point numbers not supported')
    res = []
    while num > 0:
        res.append(num % 10)
        num //= 10
    return res

def toString(num, emptyZero=False):
    if num < CUTOFF:
        digitlist = digits(num)
        if digitlist:
            res = reversed([ ROMAN_CONSTANTS[order][digit] for order, digit in enumerate(digitlist) ])
            return "".join(res)
        else:
            return "" if emptyZero else ROMAN_NOUGHT
    else:
        if num % 1 != 0.0:
            raise Exception('floating point numbers not supported')
        # For numbers over or equal the CUTOFF, the remainder of division by 2900
        # is represented as above, prepended with the multiples of MMCM (2900 in Roman),
        # which guarantees no more than 3 repetitive Ms.
        return BIG_ROMAN * (num // BIG_DEC) + toString(num % BIG_DEC, emptyZero=True)

def parse(numeral):
    numeral = numeral.upper()
    result = 0
    if numeral == ROMAN_NOUGHT.upper():
        return result
    lastVal = 0
    lastCount = 0
    subtraction = False
    for symbol in numeral[::-1]:
        value = ROMAN_SYMBOL_MAP.get(symbol)
        if not value:
            return False
            #raise Exception('incorrect symbol')
        if lastVal == 0:
            lastCount = 1
            lastVal = value
        elif lastVal == value:
            lastCount += 1
            # exceptions
        else:
            result += (-1 if subtraction else 1) * lastVal * lastCount
            subtraction = lastVal > value
            lastCount = 1
            lastVal = value
    return result + (-1 if subtraction else 1) * lastVal * lastCount

greek_alphabet = {
    u'\u0391': 'Alpha',
    u'\u0392': 'Beta',
    u'\u0393': 'Gamma',
    u'\u0394': 'Delta',
    u'\u0395': 'Epsilon',
    u'\u0396': 'Zeta',
    u'\u0397': 'Eta',
    u'\u0398': 'Theta',
    u'\u0399': 'Iota',
    u'\u039A': 'Kappa',
    u'\u039B': 'Lamda',
    u'\u039C': 'Mu',
    u'\u039D': 'Nu',
    u'\u039E': 'Xi',
    u'\u039F': 'Omicron',
    u'\u03A0': 'Pi',
    u'\u03A1': 'Rho',
    u'\u03A3': 'Sigma',
    u'\u03A4': 'Tau',
    u'\u03A5': 'Upsilon',
    u'\u03A6': 'Phi',
    u'\u03A7': 'Chi',
    u'\u03A8': 'Psi',
    u'\u03A9': 'Omega',
    u'\u03B1': 'alpha',
    u'\u03B2': 'beta',
    u'\u03B3': 'gamma',
    u'\u03B4': 'delta',
    u'\u03B5': 'epsilon',
    u'\u03B6': 'zeta',
    u'\u03B7': 'eta',
    u'\u03B8': 'theta',
    u'\u03B9': 'iota',
    u'\u03BA': 'kappa',
    u'\u03BB': 'lamda',
    u'\u03BC': 'mu',
    u'\u03BD': 'nu',
    u'\u03BE': 'xi',
    u'\u03BF': 'omicron',
    u'\u03C0': 'pi',
    u'\u03C1': 'rho',
    u'\u03C3': 'sigma',
    u'\u03C4': 'tau',
    u'\u03C5': 'upsilon',
    u'\u03C6': 'phi',
    u'\u03C7': 'chi',
    u'\u03C8': 'psi',
    u'\u03C9': 'omega',
}
