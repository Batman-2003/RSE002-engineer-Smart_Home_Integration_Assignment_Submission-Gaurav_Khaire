from datetime import datetime
import http.client
from numpy import random
from time import sleep

from Task2_CentralControlSystem import HTTP_HOST, HTTP_PORT

conn = http.client.HTTPConnection(HTTP_HOST, HTTP_PORT)
for _ in range(10_000):
    conn.request('POST', '/', body=f"{datetime.now()} | {random.randint(0, 1024)}")
    conn.close()
    # conn.send(bytes(f"{datetime.now()} | {random.randint(0, 1024)}", 'utf-8'))
    print(f"HTTPCounter: {_}")
    sleep(0.01)