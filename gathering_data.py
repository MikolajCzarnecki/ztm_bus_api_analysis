import os
import requests
import scrapper.scrapper as sc
import datetime


my_key = 'f7bce48b-6a00-4b56-879e-28f6cd90ec89'

how_many_points = 3

data_list = list()

scrapper = sc.Scrapper(my_key)


scrapper.collect_data(60, "data_1501__22_2_2024.csv")

print("Collected rows: " + str(len(scrapper.collected_data)))




