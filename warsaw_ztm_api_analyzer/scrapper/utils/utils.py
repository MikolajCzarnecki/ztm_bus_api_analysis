import datetime
from math import fabs


def busdata_to_datetime(bus_time_str: str) -> datetime.datetime:
    dtime = datetime.datetime.strptime(bus_time_str, '%Y-%m-%d %H:%M:%S')
    return dtime


def busdata_close_to_datetime(bus_date: str, measurement_dtime: datetime.datetime, tolerance: int) -> bool:
    try:
        bus_dtime = busdata_to_datetime(bus_date)

        delta_time = fabs((bus_dtime - measurement_dtime).total_seconds())

        if delta_time <= tolerance:
            return True
        else:
            return False
    except ValueError:
        print("Date in bus data is in wrong format")
    
    
def time_to_str(dtime: datetime.datetime) -> str:
    dstring = dtime.strftime('%H:%M:%S')

    return dstring


def lon_to_km(lon):
    # https://www.movable-type.co.uk/scripts/latlong.html

    return lon * 111.2


def lat_to_km(lat):
    # https://www.movable-type.co.uk/scripts/latlong.html

    return lat * 68.46
