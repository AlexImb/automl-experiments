import h2o
from h2o.automl import H2OAutoML
from kafka import KafkaConsumer
import pandas as pd
from io import StringIO

h2o.init()
h2o.cluster().timezone = "America/Los_Angeles"

# Fetch Airlines Dataset from S3
# Airlines Full Dataset 120 GB
data_path = "https://s3.amazonaws.com/h2o-airlines-unpacked/allyears_10.csv"
# Airlines all years 1987-2008 12GB
data_path = "https://s3.amazonaws.com/h2o-airlines-unpacked/allyears.csv"
# 2000 Row 4.5 MB
data_path = "https://s3.amazonaws.com/h2o-airlines-unpacked/allyears2k.csv"
# df = h2o.import_file(data_path)

# # Or use local version
df = h2o.upload_file("./datasets/allyears2k.csv")
column_names = df.names

# # Or ingest from Kafka topic
# DATA_TOPIC = 'airlines_stream'
# consumer = KafkaConsumer(
#     DATA_TOPIC, 
#     # group_id='h2o-airlines-trainer',
#     group_id=None,
#     auto_offset_reset='earliest',
#     value_deserializer=lambda x: x.decode('utf-8')
# )

# pandas_dfs = []
# # No of messages to be included in the DataFrame
# n = 3000
# i = 0
# for msg in consumer:
#     if i >= n: break
#     else:
#         # print('Message', i, ': ', msg.value)
#         if i % 100:
#             print('#', i)
    
#         if i > 0:
#             message_df = pd.read_csv(StringIO(msg.value), header = None)
#             pandas_dfs.append(message_df)
#         i += 1

# consumer.close()
# pandas_df = pd.concat(pandas_dfs) 
# df = h2o.H2OFrame(pandas_df)
# df.names = column_names

print(f'Size of training set: {df.shape[0]} rows and {df.shape[1]} columns')

df["Month"]= df["Month"].asfactor()
df["DayOfWeek"] = df["DayOfWeek"].asfactor()
df["Cancelled"] = df["Cancelled"].asfactor()
df['FlightNum'] = df['FlightNum'].asfactor()

splits= df.split_frame(ratios = [.8], seed = 1)
train = splits[0]
test = splits[1]

y = "IsDepDelayed" 
x = ["Origin", "Dest", "UniqueCarrier", "DayOfWeek", "Month", "Distance", "FlightNum"]

aml = H2OAutoML(max_runtime_secs=120, seed=1)
aml.train(x=x, y=y, training_frame=train, leaderboard_frame=test)

# Print AutoML Leaderboard
lb = aml.leaderboard
print(lb.head(rows=lb.nrows))

# Print leader model
# print(aml.leader)

# Serialize model to binary format
h2o.save_model(aml.leader, path="./models/airlines_h2o_bin")
