
from paho.mqtt.client import Client

TEMP_TOPIC = "temperature"
HUMIDITY_TOPIC = "humidity"

def on_message(mqttc, data, msg):
    print(f"Received message: {msg.topic}:{msg.payload}:{data}")
    if data["status"] == 0:
        temp = int(msg.payload) 
        if temp > data["temp_threshold"]:
            print(f"Temperature threshold exceeded ({temp}), subscribing to humidity topic")
            mqttc.subscribe(HUMIDITY_TOPIC)
            data["status"] = 1
    elif data["status"] == 1:
        if msg.topic == HUMIDITY_TOPIC:
            humidity = int(msg.payload)
            if humidity > data["humidity_threshold"]:
                print(f"Humidity threshold exceeded ({humidity}), cancelling subscription to humidity topic")
                mqttc.unsubscribe(HUMIDITY_TOPIC) 
                data["status"] = 0
        elif TEMP_TOPIC in msg.topic:
            temp = int(msg.payload)
            if temp <= data["temp_threshold"]:
                print(f"Temperature ({temp}) is below the threshold, cancelling subscription to humidity topic")
                data["status"] = 0
                mqttc.unsubscribe(HUMIDITY_TOPIC)
                
def on_log(mqttc, data, level, buf):
    print(f"LOG: {data}:{buf}")
    
def main(broker):
    data = {"temp_threshold": 20,
            "humidity_threshold": 80,
            "status": 0}
    mqttc = Client(userdata=data)
    mqttc.on_message = on_message
    mqttc.enable_logger()
    mqttc.connect(broker)
    mqttc.subscribe(f"{TEMP_TOPIC}/t1")
    mqttc.loop_forever()
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)