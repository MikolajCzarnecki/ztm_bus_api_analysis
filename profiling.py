import cProfile, pstats, io
from pstats import SortKey
import pandas as pd

from analyzer.bus_data import Bus_data as bd


pr = cProfile.Profile()
pr.enable()

test_data = bd('data_2046__21_2_2024.csv')

north = 52.349191
south = 52.127928
east = 21.2208
west = 20.857758
intervals_lon = 100
intervals_lat = 100

too_fast_realistic = test_data.too_fast(50,80)

df_grid = bd.make_grid(too_fast_realistic, north, south, west, east, intervals_lat, intervals_lon)

alpha1 = bd.make_alpha(df_grid)

pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())