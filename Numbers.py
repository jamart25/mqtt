
from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
import random

NUMBERS_TOPIC = "numbers"
TIMER_STOP_TOPIC = "timerstop"

def is_prime(n):
    i = 2
    while i*i < n and n % i != 0:
        i += 1
    return i*i > n

def timer(time, mqttc):
    mqttc.publish(TIMER_STOP_TOPIC, f"timer working. timeout: {time}")
    sleep(time)
    mqttc.publish(TIMER_STOP_TOPIC, f"timer end working")
    
def on_message(mqttc, userdata, msg):
    print(f"MESSAGE: {msg.topic}: {msg.payload}")
    try:
        if int(msg.payload) % 2 == 0:
            worker = Process(target=timer, args=(random.random()*20, mqttc))
            worker.start()
    except ValueError as e:
        print(e)
        pass

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)
    
def main(broker):
    mqttc = Client(client_id="combine_numbers")
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(NUMBERS_TOPIC)
    mqttc.loop_forever()
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)