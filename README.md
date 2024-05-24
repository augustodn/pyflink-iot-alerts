# Kafka Sensor Data Pipeline

This project demonstrates a Kafka producer that generates random sensor data and a PyFlink consumer that processes the data to detect high temperatures. The project uses Poetry for dependency management.

## Prerequisites

- Java (required for PyFlink)

## Installation

### Kafka and Zookeeper Setup

1. **Download and Extract Kafka**:
   ```sh
   wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
   tar -xzf kafka_2.13-3.7.0.tgz
   cd kafka_2.13-3.7.0
   ```

2. **Start Zookeeper**:
   ```sh
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```

   ⚠️ **Note:** The first run can ask for building the project. It will show you a message similar to this one

   ```sh
   Classpath is empty. Please build the project first e.g. by running './gradlew jar -PscalaVersion=2.13.12'
   ```

   If it's the case then run:

   ```sh
   ./gradlew jar -PscalaVersion=2.13.12
   ```

3. **Start Kafka**:
   ```sh
   bin/kafka-server-start.sh config/server.properties
   ```

4. **Create Kafka Topic**:
   ```sh
   bin/kafka-topics.sh --create --bootstrap-server localhost:9092 \
   --replication-factor 1 --partitions 1 --topic sensors
   ```

### Poetry Setup

1. **Install Poetry**:
   ```sh
   pip install poetry
   ```

2. **Clone the Repository**:
   ```sh
   git clone https://github.com/augustodn/pyflink-iot-alerts.git
   cd pyflink-iot-alerts
   ```


3. **Install pyenv**:

    **Note**: You can skip this step if you already have `pyenv` installed.
    This step is OS dependent, please follow the instructions in the official
    [repository.](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

    In **Ubuntu** you can install it using

   ```sh
   sudo apt install -y make build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
   ```

   Download and execute the `pyenv` installer script:

   ```sh
   curl https://pyenv.run | bash
   ```

   Post installation, you will have to setup `pyenv` in the shell.

   ```sh
   echo -e 'export PYENV_ROOT="$HOME/.pyenv"\nexport PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
   echo -e 'eval "$(pyenv init --path)"\neval "$(pyenv init -)"' >> ~/.bashrc
   source ~/.bashrc
   ```

   Finally you will have to install the python version you want to use.

   ```sh
   pyenv install 3.10
   pyenv local 3.10
   ```

4. **Install Dependencies**:
   ```sh
   poetry install
   ```

**Note**: Alternatively you can use conda, miniconda or any other package manager. To setup the environment. A `requirements.txt` file is also provided.

### PyFlink Setup

1. **Download and Install Java** (if not already installed):
   ```sh
   sudo apt-get update
   sudo apt-get install default-jdk
   ```

2. **Download the Flink Kafka Connector JAR**:
   ```sh
   wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.1.0-1.18/flink-sql-connector-kafka-3.1.0-1.18.jar
   ```

## Configuration

Ensure the Kafka bootstrap servers and topic configurations match in both `kafka_producer.py` and `kafka_consumer.py`.

### Kafka Producer Configuration

Edit `kafka_producer.py` if necessary to update Kafka bootstrap servers and topic.

### PyFlink Consumer Configuration

Edit `kafka_consumer.py` to update the path to the Flink Kafka Connector JAR file and other configurations if needed.

## Usage

### Running the Kafka Producer

1. **Activate the Poetry Shell**:
   ```sh
   poetry shell
   ```

2. **Run the Kafka Producer**:
   ```sh
   python kafka_producer.py
   ```

### Running the PyFlink Consumer

1. **Ensure Kafka and Zookeeper are Running**.

2. **Run the PyFlink Consumer**:
   ```sh
   python kafka_consumer.py
   ```

### Monitoring the Data Stream

- The Kafka producer will continuously generate sensor data.
- The PyFlink consumer will process the data and print alerts for high temperatures.

## Notes

- Adjust the temperature threshold in `kafka_consumer.py` as needed.
- Ensure that the Kafka topic (`sensors`) exists and is properly configured.

## License

This project is licensed under the MIT License.
