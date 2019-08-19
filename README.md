# Door Page

You've gotten halfway down the sidewalk. Did you lock the door? Pull up this
web app to check.

This project uses [`pipenv`](https://pipenv.readthedocs.io/en/latest/install/);
run `pipenv shell` to set up an environment for it.

![Locked screenshot](img/screenshot.png)

## Hardware

* ESP8266 WiFi microchip such as [this ESP8266 development board](https://www.amazon.com/Makerfocus-ESP8266-ESP-12E-Internet-Development/dp/B01IK9GEQG/)
* [HC-SR04](https://www.sparkfun.com/products/15569) ultrasonic distance sensor

The ESP8266 board linked above provides 5v output suitable for the distance
sensor. Connect the sensor's Vcc to Vin, its Trig to D4, its Echo to D3, and
its Gnd to Gnd.

## Software Setup

### Flashing the firmware

Assuming the MakerFocus board linked above:

1. Download the [Arduino IDE](https://www.arduino.cc/en/Main/Software).
2. Set up the Arduino IDE to use the board: File > Preferences and copy to "Additional Boards Manager URLs": `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
3. Go to Tools > Board > Board Manager, search for "esp8266" and install _esp8266_ by _ESP8266 Community_.
4. Set up the flash settings:
   Tools > Board > NodeMCU 1.0 (ESP-12E Module)
   Tools > Flash Size > 4M (3M SPIFFS)
   Tools > CPU Frequency > 80 Mhz
   Tools > Upload Speed > 921600
5. Download and run the NodeMCU flasher: [32-bit](https://github.com/nodemcu/nodemcu-flasher/tree/master/Win32/Release) [64-bit](https://github.com/nodemcu/nodemcu-flasher/tree/master/Win64/Release)
6. Set Tools > Port to the port that appeared after flashing.
7. Test flashing the board with an example program to blink the LED: File > Examples > ESP8266 > Blink. Click "Upload."
8. Get the WiFi library: Tools > Manage Libraries, search for "WiFiManager" and install _WiFiManager_ by _tapzu_.
9. Upload the `ultrasonic_wifi` project from the directory of the same name. If successful, the ESP8266 will create an unsecured WiFi network `UltrasonicAP`.

### Configuring

1. Connect to the configuration network, and enter WiFi credentials for the board to use. If you prefer, you can enter a second string to the `wifiManager.autoConnect()` call to specify a password, or replace it with a call to `WiFiManager.connectWifi()` to hardcode credentials.
2. Determine its IP either by checking your router / DHCP server, or by observing the board's serial output.
3. Visit the IP with a browser and fiddle with sensor placement / determine boundary values for locked and unlocked.
4. Copy `config.py.sample` to `config.py` and fill in the boundary values and IP.
5. Start the web app either with something like `env FLASK_APP=door python3 -m flask run` or with a proper web server using WSGI.
