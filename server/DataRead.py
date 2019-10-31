from datetime import datetime
import random
import time
import os
import csv
from csv import reader
import argparse
from influxdb import client as influxdb


db = influxdb.InfluxDBClient("127.0.0.1", 8086, "", "", "stocks")


def read_data(filename):
    print(filename)
    with open(filename) as f:
        lines = f.readlines()[1:]
    return lines

if __name__ == '__main__':
    filename = r"meterusage.csv"
    lines = read_data(filename)
    for rawline in lines:
        line = rawline.split(",")
        datetime_object = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
        #EVERYTHING UP TO HERE WORKS. Not sure how to create the json below
        #====================================
        json_body = [
        {
            "measurement": "usage",
            "time": datetime_object,
            "fields": {
                "meterusage": float(line[1].strip())
            }
        }
        ]

        print(json_body)

        db.write_points(json_body)