import json

from pyflink.common import Types, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaOffsetsInitializer, KafkaSource


def parse_and_filter(value: str) -> str | None:
    TEMP_THRESHOLD = 30.0
    data = json.loads(value)
    sensor_id = data["sensor_id"]
    temperature = data["data"]["temperature"]
    timestamp = data["timestamp"]
    if temperature > TEMP_THRESHOLD:  # Change 30.0 to your threshold
        alert_message = {
            "sensor_id": sensor_id,
            "temperature": temperature,
            "alert": "High temperature detected",
            "timestamp": timestamp
        }
        return json.dumps(alert_message)
    return None


def main() -> None:
    # Create a StreamExecutionEnvironment
    env = StreamExecutionEnvironment.get_execution_environment()

    # Adding the jar to my streming environment.
    env.add_jars(
        "file:///home/augusto/dev/flink/table_api_tutorial/flink-sql-connector-kafka-3.1.0-1.18.jar"
    )

    properties = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "iot-sensors",
    }

    earliest = False
    offset = (
        KafkaOffsetsInitializer.earliest()
        if earliest
        else KafkaOffsetsInitializer.latest()
    )

    # Create a Kafka Source
    # NOTE: FlinkKafkaConsumer class is deprecated
    kafka_source = (
        KafkaSource.builder()
        .set_topics("sensors")
        .set_properties(properties)
        .set_starting_offsets(offset)
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )

    # Create a DataStream from the Kafka source and assign timestamps and watermarks
    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.for_monotonous_timestamps(), "Kafka Source"
    )

    # Print line for readablity in the console
    print("start reading data from kafka")

    # Different ways of printing each event
    # Standard Print
    # data_stream.print()

    # Print with a unique ID for each event
    # data_stream.map(lambda x: f"Processed: {x}").print()

    alerts = data_stream.map(parse_and_filter).filter(lambda x: x is not None)
    alerts.print()

    # Print in a more readable format
    # data_stream.map(lambda x: f"\n{x}", output_type=Types.STRING()).print()

    # Execute the Flink pipeline
    env.execute("Kafka Sensor Consumer")


if __name__ == "__main__":
    main()
