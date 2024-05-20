#!/bin/bash

# Start kafka services

# Start zookeeper and get the PID
cd kafka-3.*-src/ && bin/zookeeper-server-start.sh config/zookeeper.properties &
# Start kafka
bin/kafka-server-start.sh config/server.properties &
# Create sensors topic
bin/kafka-topics.sh \
    --create \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1 \
    --topic sensors &
sleep(5)
../python kafka-producer.py &