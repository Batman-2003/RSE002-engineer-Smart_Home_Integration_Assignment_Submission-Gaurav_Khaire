# RSE002 - Gaurav Khaire

Video: [https://youtu.be/ChVSlVQo2vI?si=ukW0cJ6NV60_60jO] <br>

I tried to have as less dependencies as possible <br>
Dependencies: paho-mqtt, matplotlib <br> 
`pip install paho-mqtt matplotlib`<br>

Downloads: mosquitto -> [https://mosquitto.org/download/](https://mosquitto.org/download/) <br>

Instructions to Build (Windows 10) : <br>
1. Unzip the archive
2. Create a python virtual environment using pip ( or conda I have never used it).
3. Activate the virtual environment
4. Run ‘pip install matplotlib paho-mqtt’
5. Install mosquitto broker from https://mosquitto.org/download/ and run the executable.
6. NOTE: You may want to <b>skip Task3</b> as I had created the database from sqlite3 itself and not python, and size of database got upto 2gb so, <br>
the zip and repo will not include it. (Again, I might update the repo such that this doesn’t happen but, that will take time as I will also refactor many things) <br>
Run Task2 > Task1(4 different scripts) > Task3 > Task4 … in that order.




Design Doc: <br>
![Alt text](./Images/PlanOfAction.png) 

References: <br>
 TCP -> [https://www.neuralnine.com/tcp-chat-in-python/](https://www.neuralnine.com/tcp-chat-in-python/) <br>
MQTT -> [https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923](https://medium.com/@potekh.anastasia/a-beginners-guide-to-mqtt-understanding-mqtt-mosquitto-broker-and-paho-python-mqtt-client-990822274923) <br>

