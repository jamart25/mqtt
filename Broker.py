
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(userdata["topic"])
    else:
        print("Failed to connect to MQTT broker, return code: ", rc)
        
def on_message(client, userdata, msg):
    print("Received message on topic:", msg.topic)
    client.publish("clients/test", msg.payload)
    
def main(broker, topic):
    client = mqtt.Client(userdata={"topic": topic})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker)
    client.loop_forever()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} broker topic")
        sys.exit(1)
    broker = sys.argv[1]
    topic = sys.argv[2]
    main(broker, topic)