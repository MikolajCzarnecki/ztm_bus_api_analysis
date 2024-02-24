import os
import requests
import datetime
import time
import csv
from scrapper.utils.utils import busdata_close_to_datetime, time_to_str
from math import fabs


class Scrapper:
    def __init__(self, my_key):
        self.my_key = my_key
        self.resource_id = 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'
        self.type = 1
        self.url = "https://api.um.warszawa.pl/api/action/busestrams_get/"
        self.interval_sec = 60
        self.collected_data = list()

    def get_data(self):
        len_at_beginning = len(self.collected_data)

        payload = {'resource_id' : self.resource_id, 'apikey' : self.my_key, 'type' : '1'}
        
        time_now = datetime.datetime.now()
        
        response = requests.get(url=self.url, params=payload)

        response_list = response.json()['result']

        for bus_data in response_list:
            if all(key in bus_data for key in ['VehicleNumber', 'Time', 'Lon', 'Lat', 'Lines']):
                if busdata_close_to_datetime(bus_data['Time'], time_now, 180):
                    data_line = [bus_data['VehicleNumber'], bus_data['Time'],\
                                bus_data['Lon'], bus_data['Lat'],\
                                bus_data['Lines']]

                    self.collected_data.append(data_line)
            else:
                print("Server did not respond to request")
                return

        len_at_end = len(self.collected_data)

        print(time_to_str(time_now) + " - added " + str(len_at_end - len_at_beginning) + " lines of data")

    def wait_for_response(self):
        print("Trying to get response from server")
        exp = 0.5

        while True:
            payload = {'resource_id' : self.resource_id, 'apikey' : self.my_key, 'type' : '1'}
            response = requests.get(url=self.url, params=payload)

            response_list = response.json()['result']
        
            if all(key in response_list[1] for key in ['VehicleNumber', 'Time', 'Lon', 'Lat', 'Lines']):
                print("Response acquired")
                time.sleep(self.interval_sec)
                return
            else:
                print("Waiting for server to respond for " + str(exp * self.interval_sec) + " seconds...")
                time.sleep(exp * self.interval_sec)
                exp *= 2
                if exp > 17:
                    print("Server does not respond")
                    exit()

    def collect_data(self, how_many, filename):
        
        self.wait_for_response()
        
        headers = ['VehicleNumber', 'Time', 'Longitude', 'Lattitude', 'Line']

        self.collected_data.append(headers)

        for i in range(how_many):
            start_time = time.time()

            self.get_data()

            end_time = time.time()

            elapsed_time = end_time - start_time

            remaining_time = max(self.interval_sec - elapsed_time, 0)

            if i != how_many - 1:
                time.sleep(remaining_time)

        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(self.collected_data)
