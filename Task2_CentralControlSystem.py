import csv
import http.server
import os
import paho.mqtt.client as paho
import socket
import socketserver
from time import sleep
import threading


# --- Constants
# TCP_HOST = # socket.gethostname()
TCP_PORT = 42069        # VERY PROFESSIONAL :]
TCP_HEADER_SIZE = 64
TCP_DISCONNECT_MSG = '!DISCONNECT'

HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8000

MQTT_ADDR = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'MQTT_TOPIC'

LOG_CSV = 'logging.csv'
BUFFER_CSV = 'buffer.csv'
# ...

clientAddrSmoke = 0
mqttSensorStarted = False

# --- Database Related Funcs (external)
# NOTE: OK for Debugging but, not optimal at all
time_smoke = []; time_temp = []; time_humidity = []; time_motion = []
val_smoke  = []; val_temp  = []; val_humidity  = []; val_motion  = []

def clearAll():
    global time_motion, time_temp, time_smoke, time_humidity
    global val_motion, val_temp, val_smoke, val_humidity

    time_motion.clear(); time_temp.clear(); time_smoke.clear(); time_humidity.clear()
    val_motion.clear(); val_temp.clear(), val_smoke.clear(), val_humidity.clear()

def getAllSensorTimes() -> list[list[str]]:
    global time_smoke, time_temp, time_humidity, time_motion

    timesToReturn = [time_smoke ,time_temp, time_humidity, time_motion]
    return timesToReturn

def getAllSensorValues() -> list[list[int]]:
    global val_smoke  ,val_temp  ,val_humidity  ,val_motion


    valuesToReturn = [val_smoke, val_temp, val_humidity, val_motion]
    clearAll()

    return valuesToReturn
# ...

# --- Middleware Related Funcs (internal)

def parseMyMsg(data: str) -> list[str, int]:
    time, val = data.strip().split('|')
    return time, int(val)

# TCP
def tcpServer():
    global clientAddrSmoke, time_smoke, val_smoke, time_temp, val_temp
    def clientHandler(clientSoc: socket.socket, clientAddr):
        def cleanup():
            clientSoc.close()
            os._exit(-1)
        try:
            while True:
                msg = (clientSoc.recv(TCP_HEADER_SIZE)).decode('utf-8')
                if msg == TCP_DISCONNECT_MSG:
                    cleanup(); break
                print(f"TCP {clientAddr} -> {msg}")
                currTime, currVal = parseMyMsg(msg)
                if mqttSensorStarted:
                    if clientAddr == clientAddrSmoke:
                        time_smoke.append(currTime); val_smoke.append(currVal)
                    else:
                        time_temp.append(currTime); val_temp.append(currVal)

        except KeyboardInterrupt:
            print("Keyboard Interrupt: Cleaning Up")
            cleanup()
        except Exception:
            print("Unknown Exception: Cleaning Up")
            cleanup()
    
    servSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSoc.bind((socket.gethostname(), TCP_PORT))
    servSoc.listen(5)

    for _ in range(2):
        clientSoc, addr = servSoc.accept()  # WARNING: This is blocking
        print(f"TCP Connection to {addr} established. ")
        if _ == 0:
            clientAddrSmoke = addr  # Jugaad

        tcp_thread = threading.Thread(target=clientHandler, args=(clientSoc, addr))
        tcp_thread.start()
    
# HTTP
class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self: http.server.BaseHTTPRequestHandler):
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print("Got a POST Request")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        currTime, currVal = parseMyMsg(self.rfile.read().decode('utf-8'))

        if mqttSensorStarted:
            time_humidity.append(currTime); val_humidity.append(currVal)

def httpServerHandler():
    with socketserver.TCPServer((HTTP_HOST, HTTP_PORT), MyHTTPRequestHandler) as httpd:
        print(f"Serving at HTTP Host: {HTTP_HOST}")
        print(f"Serving at HTTP Port: {HTTP_PORT}")
        httpd.serve_forever()

def httpServer():
    http_thread = threading.Thread(target=httpServerHandler)
    http_thread.start()

# MQTT
def mqttSubscriberCallback(client, userdata, msg: paho.MQTTMessage):
    global time_motion, val_motion, mqttSensorStarted
    print("------------------------------------------------------------")
    print(f"MQTT: {msg.topic}: {msg.payload.decode()}")
    print("------------------------------------------------------------")
    if mqttSensorStarted == False:
        mqttSensorStarted = True
        clearAll()
    currTime, currVal = parseMyMsg(msg.payload.decode())
    time_motion.append(currTime); val_motion.append(currVal)

def mqttServerHandler():
    subscriber = paho.Client()
    subscriber.on_message = mqttSubscriberCallback
    if subscriber.connect(MQTT_ADDR, MQTT_PORT) != 0:
        print("Error Connecting to Broker: Make Sure Mosquitto is Running")
        os._exit(-1)
    subscriber.subscribe(MQTT_TOPIC)

    try:
        print("MQTT: Subscribing ... Press Ctrl + C to stop")
        subscriber.loop_forever()
    except Exception as e:
        print("MQTT: Unknown Exception Exitting")
        print(e)
    finally:
        subscriber.disconnect()
        print("MQTT: Disconnected")

def mqttServer():
    mqtt_thread = threading.Thread(target=mqttServerHandler)
    mqtt_thread.start()

def writeToCsv():
    global time_smoke, time_temp, time_humidity, time_motion
    global val_smoke, val_temp, val_humidity, val_motion
    loopLength = min(len(time_smoke), len(time_temp), len(time_humidity), len(time_motion))

    csvFile = open(f'Data_Collection\\{LOG_CSV}', 'a')
    csvWriter = csv.writer(csvFile)
    for _ in range(loopLength):
        csvWriter.writerow([time_smoke[_], val_smoke[_],
                            time_temp[_],  val_temp[_],
                            time_humidity[_], val_humidity[_],
                            time_motion[_], val_motion[_]])
    csvFile.close()

    csvFile = open(f'Data_Collection\\{BUFFER_CSV}', 'a')
    csvWriter = csv.writer(csvFile)
    for _ in range(loopLength):
        csvWriter.writerow([val_smoke[_],
                            val_temp[_],
                            val_humidity[_],
                            val_motion[_]])
    csvFile.close()
    clearAll()

# ...

def main():
    global time_motion, val_humidity, time_smoke, val_temp
    tcpServer()     # These are 2 servers on 2 threads actually, bad func-name
    httpServer()
    mqttServer()
    try:
        while True:
            if len(time_motion) > 0:    # Wait till motion_sensor starts
                writeToCsv()
            sleep(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Closing Now")
        print(f"time_motion: {time_motion[:10]}")
        print(f"val_humidity: {val_humidity[:10]}")
        print(f"time_smoke: {time_smoke[:10]}")
        print(f"val_temp: {val_temp[:10]}")
        os._exit(-1)


if __name__ == '__main__':
    main()