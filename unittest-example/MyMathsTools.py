import math


def deg2rad(deg):
    return deg * (math.pi/180)


def sin_deg(deg, inverse=False):
    if not inverse:
        return math.sin(deg2rad(deg))
    else:
        return 1 / math.sin(deg2rad(deg))


def cos_deg(deg):
    return math.cos(deg2rad(deg))
