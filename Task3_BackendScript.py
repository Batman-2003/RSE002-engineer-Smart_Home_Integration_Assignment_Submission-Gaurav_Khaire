import sqlite3
from time import sleep
import numpy as np
import csv
import os
from Task2_CentralControlSystem import LOG_CSV

# TODO: 1. Add some Error Handling to all these Functions
# TODO: 2. Try to insert in bulk instead of one query at a time... maybe 10 ?

DATABASE = 'Data_Collection\\sensors.db' # Windows Only

MOTION_TABLE   = 'Motion_Sens'
TEMP_TABLE     = 'Temp_Sens'
SMOKE_TABLE    = 'Smoke_Sens'
HUMIDITY_TABLE = 'Humidity_Sens'

# WARNING: GLOBAL VARS

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


def insert_motion(time, val):
    conn.execute(f"INSERT INTO {MOTION_TABLE} VALUES ('{time}', {val});")
    # conn.commit()

def insert_temp(time, val):
    conn.execute(f"INSERT INTO {TEMP_TABLE} VALUES ('{time}', {val});")
    # conn.commit()

def insert_smoke(time, val):
    conn.execute(f"INSERT INTO {SMOKE_TABLE} VALUES ('{time}', {val});")
    # conn.commit()

def insert_humidity(time, val):
    conn.execute(f"INSERT INTO {HUMIDITY_TABLE} VALUES ('{time}', {val});")
    # conn.commit()

def main():
    db_time_smoke = []; db_time_temp = []; db_time_humidity = []; db_time_motion = []
    db_val_smoke  = []; db_val_temp  = []; db_val_humidity  = []; db_val_motion  = []
    data = []
    
    if os.path.exists(f'Data_Collection\\{LOG_CSV}'):
        # TODO: Write the reader csv part and then, the delete csv part
        csvFile = open(f'Data_Collection\\{LOG_CSV}', 'r')
        csvReader = csv.reader(csvFile)
        for line in csvReader:
            if len(line) == 8:
                data.append(line)
        csvFile.close()
        # os.remove(f'Data_Collection\\{LOG_CSV}')
        data = np.array(data)

        db_time_smoke = data[:, 0]
        db_val_smoke  = np.array(data[:, 1], dtype=np.int64)
        db_time_temp = data[:, 2]
        db_val_temp  = np.array(data[:, 3], dtype=np.int64)
        db_time_humidity = data[:, 4]
        db_val_humidity  = np.array(data[:, 5], dtype=np.int64)
        db_time_motion = data[:, 6]
        db_val_motion  = np.array(data[:, 7], dtype=np.int64)

        # Insert all the data 1 by 1 ... should do it in bulk instead
        for t_smoke, v_smoke in zip(db_time_smoke, db_val_smoke):
            insert_smoke(t_smoke, v_smoke)
        # db_time_smoke.clear(); db_val_smoke.clear()
        conn.commit()
        print(f"INSERTED DATA INTO smoke")

        for t_temp, v_temp in zip(db_time_temp, db_val_temp):
            insert_temp(t_temp, v_temp)
        # db_time_temp.clear(); db_val_temp.clear()
        conn.commit()
        print(f"INSERTED DATA INTO temp")

        for t_humidity, v_humidity in zip(db_time_humidity, db_val_humidity):
            insert_humidity(t_humidity, v_humidity)
        # db_time_humidity.clear(); db_val_humidity.clear()
        conn.commit()
        print(f"INSERTED DATA INTO humidity")

        for t_motion, v_motion in zip(db_time_motion, db_val_motion):
            insert_motion(t_motion, v_motion)
        # db_time_motion.clear(); db_val_motion.clear()
        conn.commit()
        print(f"INSERTED DATA INTO motion")

        print(f"db_time_smoke: {db_time_smoke}")
        print(f"db_time_motion: {db_time_motion}")
        print(f"db_val_humidity: {db_time_humidity}")

    sleep(1)


if __name__ == '__main__':
    while True:
        main()