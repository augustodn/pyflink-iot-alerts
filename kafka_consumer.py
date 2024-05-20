from pyflink.common import WatermarkStrategy, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer

# Create a StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# Adding the jar to my streming environment.
env.add_jars("file:///home/augusto/dev/flink/table_api_tutorial/flink-sql-connector-kafka-3.1.0-1.18.jar")

properties = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'iot-sensors',
}

earliest = False
offset = KafkaOffsetsInitializer.earliest() if earliest else KafkaOffsetsInitializer.latest()

# Create a Kafka Source
# NOTE: FlinkKafkaConsumer class is deprecated
kafka_source = KafkaSource.builder() \
    .set_topics("sensors") \
    .set_properties(properties) \
    .set_starting_offsets(offset) \
    .set_value_only_deserializer(SimpleStringSchema())\
    .build()

# Create a DataStream from the Kafka source and assign timestamps and watermarks
data_stream = env.from_source(kafka_source, WatermarkStrategy.for_monotonous_timestamps(), "Kafka Source")

# Print line for readablity in the console
print("start reading data from kafka")

# Different ways of printing each event
# Standard Print
# data_stream.print()

# Print with a unique ID for each event
data_stream.map(lambda x: f"Processed: {x}").print()

# Print in a more readable format
# data_stream.map(lambda x: f"\n{x}", output_type=Types.STRING()).print()

# Execute the Flink pipeline
env.execute("Kafka Sensor Consumer")
