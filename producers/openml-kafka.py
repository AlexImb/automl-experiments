"""Kafka producer from OpenML dataset"""

import os
from dotenv import load_dotenv
import openml
import time
from kafka import KafkaProducer

# Load env variables from .env file
load_dotenv()

# Load from the environment
OPENML_API_KEY = os.getenv('OPENML_API_KEY')
OPENML_PUBLISH = os.getenv('OPENML_PUBLISH', False) == 'True'

openml.config.apikey = OPENML_API_KEY

# TODO: Read from run arguments
# Adult: https://www.openml.org/d/23512
OPENML_DATASET = 23512
TOPIC = f'openml_test_4_{OPENML_DATASET}'
MAX_SAMPLES = 10000

dataset = openml.datasets.get_dataset(OPENML_DATASET)
data, categorical, attributes = dataset._load_data()

print(f'Publishing dataset ID: {OPENML_DATASET} to Kafka topic: {TOPIC}')
start_time = time.time()

producer = KafkaProducer(bootstrap_servers='broker:29092')

for i in data.index:
    producer.send(TOPIC, data.iloc[[i]].to_csv(header=False).encode('utf-8'))
    producer.flush()
    if i > MAX_SAMPLES:
        break

elapsed_time = time.time() - start_time
print('Done in: ', elapsed_time)
