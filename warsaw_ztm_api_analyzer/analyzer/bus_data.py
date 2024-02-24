import datetime
from math import fabs, sqrt
import pandas as pd
import numpy as np

from .utils.utils import get_dist, lon_to_km, lat_to_km, filter_close_to_zero

class Bus_data:
    def __init__(self, path):
        pd.options.mode.copy_on_write = True

        self.data = pd.read_csv(path)
        self.preprocess()

    def convert_coordinates_to_km(self):
        self.data['converted_lon'] = self.data.apply(lambda row: lon_to_km(row['Longitude']), axis = 1)
        self.data['converted_lat'] = self.data.apply(lambda row: lat_to_km(row['Lattitude']), axis = 1)

    def convert_time(self):
        self.data['Time'] = pd.to_datetime(self.data['Time'])

    def add_delta(self):
        self.data = self.data.sort_values(by='Time')

        self.data['time_diff'] = self.data.groupby('VehicleNumber')['Time'].diff()

        self.data['lon_diff'] = self.data.groupby('VehicleNumber')['converted_lon'].diff()
        self.data['lat_diff'] = self.data.groupby('VehicleNumber')['converted_lat'].diff()

        self.data = self.data.dropna()
        self.data['delta_dist'] = self.data.apply(lambda row: get_dist(row['lon_diff'], row['lat_diff']), axis = 1)
        self.data['time_diff'] = self.data.apply(lambda row: int(row['time_diff'].total_seconds()), axis = 1)

    def drop_still(self):
        self.data = self.data[self.data.apply(filter_close_to_zero, axis=1)]

    def add_velocity(self):
        self.data['velocity'] = self.data.apply(lambda row: (row['delta_dist'] / row['time_diff']) * 3600, axis=1)

    def preprocess(self):
        self.convert_coordinates_to_km()
        self.convert_time()
        self.add_delta()
        self.drop_still()
        self.add_velocity()

    def too_fast(self, speed_limit, unrealistic):
        ddata = self.data.copy()
        too_fast = ddata[ddata['velocity'] > speed_limit]
        too_fast_realistic = too_fast[too_fast['velocity'] < unrealistic]
        return too_fast_realistic
    
    @staticmethod
    def crop_coords(data, north, south, west, east):
        loc_speed = data[data['Lattitude'] < north]
        loc_speed = loc_speed[loc_speed['Lattitude'] > south]
        loc_speed = loc_speed[loc_speed['Longitude'] < east]
        loc_speed = loc_speed[loc_speed['Longitude'] > west]

        return loc_speed
    
    @staticmethod
    def make_grid(data, north, south, west, east, intervals_lat, intervals_lon):
        cropped_data = Bus_data.crop_coords(data, north, south, west, east)

        step_lat = (north - south) / intervals_lat
        step_lon = (east - west) / intervals_lon

        lon_space = np.linspace(west, east, intervals_lon)
        lat_space = np.linspace(south, north, intervals_lat)
        lon_axis = pd.Series(lon_space)
        lat_axis = pd.Series(lat_space)

        increased = 0

        df_grid = pd.DataFrame(0, index=lat_axis, columns=lon_axis)

        for index, row in cropped_data.iterrows():
            chosen_lat_ind = -1
            chosen_lon_ind = -1
    
            for ind_lat in range(len(df_grid.index)):
                if row['Lattitude'] > df_grid.index[ind_lat] and row['Lattitude'] < df_grid.index[ind_lat] + step_lat:
                    chosen_lat_ind = ind_lat
                    break

            for ind_lon in range(len(df_grid.columns)):
                if row['Longitude'] > df_grid.columns[ind_lon] and row['Longitude'] < df_grid.columns[ind_lon] + step_lon:
                    chosen_lon_ind = ind_lon
                    break

            if chosen_lat_ind > -1 and chosen_lon_ind > -1:
                df_grid.iloc[chosen_lat_ind, chosen_lon_ind] += 1
                df_grid.iloc[chosen_lat_ind, chosen_lon_ind] = int(df_grid.iloc[chosen_lat_ind, chosen_lon_ind])
                increased += 1

        print('increased ' + str(increased) + ' times')

        df_grid.reindex(index=df_grid.index[::-1])
        return df_grid
    
    @staticmethod
    def make_alpha(data):
        alphas = np.ones(data.shape)

        for ind_lat in range(len(data.index)):
            for ind_lon in range(len(data.columns)):
                if(data.iloc[ind_lat, ind_lon] == 0):
                    alphas[ind_lat, ind_lon] = 0
                if(data.iloc[ind_lat, ind_lon] == 1):
                    alphas[ind_lat, ind_lon] = 0.3
                if(data.iloc[ind_lat, ind_lon] == 2):
                    alphas[ind_lat, ind_lon] = 0.4
                if(data.iloc[ind_lat, ind_lon] == 3):
                    alphas[ind_lat, ind_lon] = 0.6

        return alphas

    