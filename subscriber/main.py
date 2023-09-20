import time
import machine
from modules.mqtt_client import MQTT

led = machine.Pin('LED', machine.Pin.OUT)

class Middleware:

    def __init__(self):
        self.MC = MQTT(
            client_id=b"subscriber",
            server=b"27c4ac6276f441e49d6e912f9be0e6d2.s1.eu.hivemq.cloud",
            port=0,
            user="henriquemarlon",
            password="@Lux314159",
            keepalive=7200, ssl=True,
            ssl_params={
                'server_hostname': '27c4ac6276f441e49d6e912f9be0e6d2.s1.eu.hivemq.cloud'},
            topic="result"
        )

    def routine(self):
        def callback(topic, msg):
            view = msg.decode("utf-8")
            print(f'Result: {view}')
            if view == "true":
                led.on()
                time.sleep(8)
                led.off()
            elif view == "false":
                led.off()
            else:
                print("Error on result message")
        self.MC.set_callback(callback)
        self.MC.connect()
        self.MC.subscribe()

        while True:
            self.MC.wait_message()


MW = Middleware()

if __name__ == '__main__':
    while True:
        MW.routine()