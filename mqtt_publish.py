from machine import Pin, PWM
import dht
import network
from umqtt.simple import MQTTClient
from time import sleep
import ujson

# ---------- WIFI ----------
WIFI_NAME = "Prakash d"
WIFI_PASSWORD = "prakash12#"

# ---------- MQTT ----------
BROKER = "broker.hivemq.com"
TOPIC = b"engineering/project/environment"

# ---------- SENSOR ----------
sensor = dht.DHT11(Pin(4))

# ---------- OUTPUTS ----------
led = Pin(18, Pin.OUT)
buzzer = PWM(Pin(19))

buzzer.duty_u16(0)

# ---------- CONNECT WIFI ----------
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Connecting WiFi...")

wifi.connect(WIFI_NAME, WIFI_PASSWORD)

while not wifi.isconnected():
    sleep(1)

print("WiFi Connected!")
print(wifi.ifconfig())

# ---------- CONNECT MQTT ----------
client = MQTTClient("esp32", BROKER)

print("Connecting MQTT...")

client.connect()

print("MQTT Connected!")

# ---------- LOOP ----------
while True:

    try:
        sensor.measure()

        temp = sensor.temperature()
        humidity = sensor.humidity()

        print("Temp =", temp)
        print("Humidity =", humidity)

        data = {
            "humidity": humidity,
            "temp": temp
        }

        client.publish(
            TOPIC,
            ujson.dumps(data)
        )

        print("Published:", data)

        # ALERT
        if temp > 35:
            led.on()

            buzzer.freq(1000)

            buzzer.duty_u16(30000)

            sleep(0.5)

            buzzer.duty_u16(0)

        else:

            led.off()

            buzzer.duty_u16(0)

        sleep(2)

    except Exception as e:

        print("Error:", e)

        sleep(2)
