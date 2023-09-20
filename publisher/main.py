import time
from modules.mfrc522 import MFRC522
from modules.umqtt_simple import MQTTClient


class MQTT:
    def __init__(self, client_id, server, port, user, password, keepalive, ssl, ssl_params):
        self.client_id = client_id
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.keepalive = keepalive
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.client = MQTTClient(client_id=self.client_id,
                                 server=self.server,
                                 port=self.port,
                                 user=self.user,
                                 password=self.password,
                                 keepalive=self.keepalive,
                                 ssl=self.ssl,
                                 ssl_params=self.ssl_params
                                 )

    def connect(self):
        self.client.connect()

    def publish(self, topic, msg):
        self.client.publish(topic, msg)
        print("Published: " + str(msg))
        time.sleep(2)

    def set_callback(self, callback):
        self.client.set_callback(callback)

    def wait_message(self):
        self.client.wait_msg()

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Subscribed: " + str(topic))

    def disconnect(self):
        self.client.disconnect()

class Rfid:
    def __init__(self):
        self.MC = MQTT(
            client_id=b"publisher",
            server=b"27c4ac6276f441e49d6e912f9be0e6d2.s1.eu.hivemq.cloud",
            port=0,
            user="henriquemarlon",
            password="@Lux314159",
            keepalive=7200, ssl=True,
            ssl_params={
                'server_hostname': '27c4ac6276f441e49d6e912f9be0e6d2.s1.eu.hivemq.cloud'}
        )

    def connect(self):
        self.MC.connect()

    def publish(self, topic, msg):
        self.MC.publish(topic, msg)

RF = Rfid()

RF.connect()
print("MQTT Connected")

print("Bring TAG closer...")
print("")

if __name__ == "__main__":

    reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

    while True:
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid), "little", False)
                print("CARD ID: "+str(card))
                if card == 422078531:
                    RF.publish(
                        "checkIn", "0xB847c0d4f2508373CdF06Cc1988a403C705aF6fb")