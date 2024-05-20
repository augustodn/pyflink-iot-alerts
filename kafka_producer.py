import json
import time
from datetime import datetime, timezone
import random
from kafka import KafkaProducer

def generate_sensor_data() -> dict[str, any]:
    sensor_id = f"sensor_{random.randint(1, 5)}"
    temperature = round(random.uniform(15, 35), 2)
    pressure = round(random.uniform(950, 1050), 2)
    vibration = round(random.uniform(0, 10), 2)
    sensor_data = {
        "sensor_id": sensor_id,
        "data": {
            "temperature": temperature,
            "pressure": pressure,
            "vibration": vibration
        },
        # utc timestamp
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return sensor_data

def main():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    while True:
        sensor_data = generate_sensor_data()
        producer.send('sensors', value=sensor_data)
        print(f"Produced: {sensor_data}")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
