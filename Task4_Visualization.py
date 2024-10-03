import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Task2_CentralControlSystem import BUFFER_CSV
import os
import csv

data = []

def main_loop(frame):
    global data
    if os.path.exists(f'Data_Collection\\{BUFFER_CSV}'):
        csvFile = open(f'Data_Collection\\{BUFFER_CSV}', 'r')
        csvReader = csv.reader(csvFile)
        for line in csvReader:
            if len(line) > 0:
                data.append(line)
        csvFile.close()
        # os.remove(f'Data_Collection\\{BUFFER_CSV}')

        if len(data) >= 50:
            np_data = np.array(data[len(data)-50: ], dtype=np.int32)
            x = np.arange(-49, 1, 1)
            print("")
            y0 = np.array(np_data[:, 0], dtype=np.int32)
            y1 = np.array(np_data[:, 1], dtype=np.int32)
            y2 = np.array(np_data[:, 2], dtype=np.int32)
            y3 = np.array(np_data[:, 3], dtype=np.int32)
            plt.cla()
            plt.plot(x, y0, color='red')
            plt.plot(x, y1, color='blue')
            plt.plot(x, y2, color='green')
            plt.plot(x, y3, color='orange')
            plt.legend(('SmokeTCP', 'TempTCP', 'HumidityHTTP', 'MotionMQTT'), loc='upper right')
        else:
            pass
    else:
        pass

    




if __name__ == '__main__':
    fig, ax = plt.subplots()
    animation = FuncAnimation(fig, main_loop, interval = 10)
    plt.show()
    