from threading import Lock 
from paho.mqtt.client import Client
from time import sleep


# Class to store temperature data and calculate the mean temperature for each topic
class TemperatureData:
    def __init__(self):
        self.lock = Lock()
        self.data = {}

    # Add a temperature reading to the data for a given topic
    def add_temperature(self, topic, temperature):
        n = len("temperature/")
        key = topic[n:]
        with self.lock:
            if key in self.data:
                self.data[key].append(temperature)
            else:
                self.data[key] = [temperature]

    # Get the mean temperature for each topic and reset the data
    def get_mean_temperatures(self):
        with self.lock:
            mean_temperatures = []
            for key, values in self.data.items():
                mean_temperature = sum(values) / len(values)
                mean_temperatures.append((key, mean_temperature))
                self.data[key] = []
            return mean_temperatures



def on_message(mqttc, temperature_data, msg):
    print("Received message:", msg.topic, msg.payload)
    temperature = float(msg.payload.decode('utf-8'))
    temperature_data.add_temperature(msg.topic, temperature)



def main(broker):
    temperature_data = TemperatureData()
    mqttc = Client(userdata=temperature_data)
    mqttc.on_message = lambda client, userdata, msg: on_message(client, temperature_data, msg)
    mqttc.connect(broker)
    mqttc.subscribe("temperature/#")
    mqttc.loop_start()
    while True:
        sleep(8)
        mean_temperatures = temperature_data.get_mean_temperatures()
        for key, mean_temperature in mean_temperatures:
            print(f"Mean temperature for {key}: {mean_temperature}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} broker")
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)