import h2o
from h2o.automl import H2OAutoML

h2o.init()
h2o.cluster().timezone = "America/Los_Angeles"

# Fetch Airlines Dataset from S3
# Airlines Full Dataset 120 GB
data_path = "https://s3.amazonaws.com/h2o-airlines-unpacked/allyears_10.csv"
# Airlines all years 1987-2008 12GB
data_path = "https://s3.amazonaws.com/h2o-airlines-unpacked/allyears.csv"
# 2000 Row 4.5 MB
data_path = "https://s3.amazonaws.com/h2o-airlines-unpacked/allyears2k.csv"
# airlines_df = h2o.import_file(data_path)

# Or use local version
df = h2o.upload_file("./datasets/allyears2k.csv")

print(f'Size of training set: {df.shape[0]} rows and {df.shape[1]} columns')

df["Year"]= df["Year"].asfactor()
df["Month"]= df["Month"].asfactor()
df["DayOfWeek"] = df["DayOfWeek"].asfactor()
df["Cancelled"] = df["Cancelled"].asfactor()
df['FlightNum'] = df['FlightNum'].asfactor()

splits= df.split_frame(ratios = [.8], seed = 1)
train = splits[0]
test = splits[1]

y = "IsDepDelayed" 
x = ["Origin", "Dest", "Year", "UniqueCarrier", "DayOfWeek", "Month", "Distance", "FlightNum"]

aml = H2OAutoML(max_runtime_secs=120, seed=1)
aml.train(x=x, y=y, training_frame=train, leaderboard_frame=test)

# Print AutoML Leaderboard
lb = aml.leaderboard
print(lb.head(rows=lb.nrows))

# Print leader model
# print(aml.leader)

# Serialize model to binary format
h2o.save_model(aml.leader, path="./models/airlines_h2o_bin")
