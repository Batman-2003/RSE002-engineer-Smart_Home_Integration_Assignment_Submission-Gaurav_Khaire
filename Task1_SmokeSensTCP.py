import socket
from time import sleep
from datetime import datetime
from numpy import random

from Task2_CentralControlSystem import TCP_PORT, TCP_DISCONNECT_MSG

smokeClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
smokeClientSock.connect((socket.gethostname(), TCP_PORT))

for _ in range(10_000):
    smokeClientSock.send(f"{datetime.now()} | {random.randint(0, 1024)}".encode('utf-8'))
    sleep(0.01)
    print(f"smokeCounter: {_}")
smokeClientSock.send(TCP_DISCONNECT_MSG.encode('utf-8'))