import pytest

from math import sqrt
import analyzer.utils.utils as utils
import numpy as np
import pandas as pd


@pytest.fixture
def testowe_dane():
    data = {
        'VehicleNumber': [1234, 111],
        'Longitude' : [21.11, 22.22],
        'Lattitude' : [53.33, 54.44],
        'Line' : [123, 456],
        'time_diff' : [0.0, 1.0]
    }

    dframe = pd.DataFrame(data)
    return dframe


def test_lon_to_km():
    takie_same = np.allclose(utils.lon_to_km(10), 1112.0)
    assert (takie_same, True)


def test_lat_to_km():
    takie_same = np.allclose(utils.lat_to_km(10), 684.6)
    assert (takie_same, True)


def test_not_close_to_zero(testowe_dane):
    close = utils.filter_close_to_zero(testowe_dane.iloc[0])
    assert(close, False)


def test_close_to_zero(testowe_dane):
    close = utils.filter_close_to_zero(testowe_dane.iloc[1])
    assert(close, True)


def test_dist():
    close = np.allclose(utils.get_dist(1,1), sqrt(2))
    assert(close, True)