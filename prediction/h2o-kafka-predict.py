import h2o
import csv
from kafka import KafkaConsumer, KafkaProducer

INPUT_TOPIC = 'airlines_prediction_input'
OUTPUT_TOPIC = 'airlines_prediction_output'

h2o.init()
h2o.cluster().timezone = 'America/Los_Angeles'

# Load the binary serialization of the model
model_path = 'models/airlines_h2o_bin/StackedEnsemble_AllModels_AutoML_20200104_230354'
model = h2o.load_model(model_path)

# Read column names from sample data
df = h2o.upload_file("./datasets/allyears2k.csv")
column_names = df.names

# Create a producer to send the pridction output
producer = KafkaProducer()

# Cosume Kakfa messages from the input topic
consumer = KafkaConsumer(INPUT_TOPIC, value_deserializer=lambda x: x.decode('utf-8'))
for msg in consumer:
    try:
        print('Message:', msg.value)
        parsed_csv = csv.reader([msg.value])
        parsed_csv = list(parsed_csv)
        print('Parsed', parsed_csv)
        input_df = h2o.H2OFrame(parsed_csv)
        input_df.names = column_names
        print(input_df)
        print(f'Size of input dataframe: {input_df.shape[0]} rows and {input_df.shape[1]} columns')
        predicted = model.predict(input_df)
        print('Prediction')
        print(predicted.head())
        producer.send(OUTPUT_TOPIC, predicted.get_frame_data().encode('utf-8'))
    except Exception as e:
        print('An exception occured for:', msg, e)

