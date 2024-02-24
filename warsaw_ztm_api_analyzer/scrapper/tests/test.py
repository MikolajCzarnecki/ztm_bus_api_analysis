import pytest

import scrapper.utils.utils as utils
import datetime


@pytest.fixture
def time_str():
    return '2024-3-21 21:34:56'


@pytest.fixture
def sample_datetime():
    return datetime.datetime(2024, 3, 21, 21, 34, 47)


def test_str_to_datetime(time_str):
    dt = utils.busdata_to_datetime(time_str)
    print(dt)
    dt_expected = datetime.datetime(2024, 3, 21, 21, 34, 56)

    datetime_equal = dt == dt_expected

    assert datetime_equal


def test_busdata_close(time_str, sample_datetime):
    comparison_result = utils.busdata_close_to_datetime(time_str, sample_datetime, 10)
    assert comparison_result


def test_time_to_str(sample_datetime):
    string = utils.time_to_str(sample_datetime)

    assert string == '21:34:47'
