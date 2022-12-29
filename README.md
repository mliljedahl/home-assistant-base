# home-assistant-base

An simple and easy to start with set up of Home Assistant using docker-compose.

Included components:

* Home Assistant
* PostgreSQL
* Grafana
* InfluxDB
* Z-Wave JS UI
* telldus-core
* Eclipse Mosquitto (MQTT)

# Installation

For now the [.env](#env) file needs to be manually edited and also the [install.py](#installpy) script needs to be run to generate all required passwords. The complete setup will be managed by [install.py](#installpy) in a future version.

## .env

The `.env` file holds all information about what version (tags) of the docker images to run, what ports they should run on and the **path** to *zigbee* and *zwave* devices (required to manually set).

```
# Required settings (example)
ZIGBEE_SERIAL_ID=/dev/serial/by-id/usb-dresden_elektronik_ingenieurtechnik_GmbH_ConBee_II_DE2193921-if00
ZWAVE_SERIAL_ID=/dev/serial/by-id/usb-0658_0200-if00
```

## install.py

This script generates and sets all passowrds required for the setup. Use the following to execute it:

```
$ python3 install.py
```
