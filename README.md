![Python version](https://img.shields.io/badge/python-3.10.0-blue) ![MQTT version](https://img.shields.io/badge/MQTT-3.1.1-blueviolet)

# MQTT Broker
An MQTT broker using MQTT version 3.1.1 written in Python using no external libraries outside of Python standard library. Using threads for individual sockets the broker can handle multiple simultaneous connections. Will, retain, QoS above 0, and such are not implemented. 

## Quick start
1. Clone repository:
```bash
git clone https://github.com/Adilius/MQTT-Broker-Python.git
```

2. Run broker:
```bash
python .\MQTT_Broker.py
```

## Implemented operations
* Connect/Disconnect
* Subscribe/Unsubscribe
* Ping request/response
* Publish


## Demo
Terminal running broker:

![MQTT_terminal](https://user-images.githubusercontent.com/43440295/145275297-c0d9b035-be59-4098-b6bc-042f79f096a7.gif)




Testing broker using an [MQTT client](https://mqttfx.jensd.de/) (seperate run from above gif)

![MQTT_client](https://user-images.githubusercontent.com/43440295/145275334-49d38634-4f2a-42c0-a66a-8f4dfb66cb6a.gif)
