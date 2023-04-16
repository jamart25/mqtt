from paho.mqtt.client import Client
import paho.mqtt.publish as publish
from multiprocessing import Process
from time import sleep

class MQTTWorker:
    def __init__(self, broker):
        self.broker = broker
    
    def work_on_message(self, message):
        print("process body", message)
        topic, timeout, text = message[2:-1].split(",")
        print("process body", timeout, topic, text)
        sleep(int(timeout))
        publish.single(topic, payload=text, hostname=self.broker)
        print("end process body", message)

class MQTTClient:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.mqttc = Client(userdata={"broker": broker})
        self.mqttc.enable_logger()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.worker = MQTTWorker(broker)

    def start(self):
        self.mqttc.connect(self.broker)
        self.mqttc.subscribe(self.topic)
        self.mqttc.loop_forever()

    def on_message(self, mqttc, userdata, msg):
        print("on_message", msg.topic, msg.payload)
        worker_process = Process(target=self.worker.work_on_message, args=(str(msg.payload),))
        worker_process.start()
        print("end on_message", msg.payload)

    def on_connect(self, mqttc, userdata, flags, rc):
        print("CONNECT:", userdata, flags, rc)
        
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} broker topic")
        sys.exit(1)
    broker = sys.argv[1]
    topic = sys.argv[2]
    mqtt_client = MQTTClient(broker, topic)
    mqtt_client.start()