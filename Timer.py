import paho.mqtt.client as mqtt
import random
import time


broker = "localhost"


sensor_ids = ["sensor1", "sensor2", "sensor3"]


temperature_topic = "sensors/temperature"
humidity_topic = "sensors/humidity"

# Define a function to simulate temperature and humidity readings from a sensor
def get_sensor_reading(sensor_id):
    temperature = random.uniform(18.0, 30.0)
    humidity = random.uniform(40.0, 60.0)
    return {"sensor_id": sensor_id, "temperature": temperature, "humidity": humidity}

# Define the callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    # Sensor ID from the topic
    sensor_id = message.topic.split("/")[-1]
    # Convert the payload to a string and print it out
    data = message.payload.decode()
    print(f"Received message from {sensor_id}: {data}")


def main():
    
    client = mqtt.Client()
    client.on_message = on_message
    # Connect to the MQTT broker
    client.connect(broker)
    # Subscribe to the temperature and humidity topics for each sensor
    for sensor_id in sensor_ids:
        client.subscribe(f"{temperature_topic}/{sensor_id}")
        client.subscribe(f"{humidity_topic}/{sensor_id}")
    # Start the MQTT loop 
    client.loop_start()
    # Send temperature and humidity readings every 5 seconds
    while True:
        for sensor_id in sensor_ids:
            reading = get_sensor_reading(sensor_id)
            # Publish the temperature and humidity readings for the sensor
            client.publish(f"{temperature_topic}/{sensor_id}", f"{reading['temperature']:.2f}")
            client.publish(f"{humidity_topic}/{sensor_id}", f"{reading['humidity']:.2f}")
        time.sleep(5)

if __name__ == "__main__":
    main()