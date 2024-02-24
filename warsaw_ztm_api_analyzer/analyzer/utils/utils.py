import numpy as np
from math import fabs, sqrt


def lon_to_km(lon):
    #https://www.movable-type.co.uk/scripts/latlong.html

    return lon * 111.2


def lat_to_km(lat):
    #https://www.movable-type.co.uk/scripts/latlong.html

    return lat * 68.46


def filter_close_to_zero(x):
    return not np.allclose(x['time_diff'], 0.00)


def get_dist(xdiff, ydiff) -> float:
    dist = sqrt(fabs(xdiff)**2 + fabs(ydiff)**2)
    return dist
