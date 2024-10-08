import math


def sign_or_null(v: float):
    if v == 0:
        return 0
    else:
        return math.copysign(1, v)
