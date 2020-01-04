import h2o

h2o.init()
h2o.cluster().timezone = "America/Los_Angeles"

model_path = 'models/airlines_h2o_bin/StackedEnsemble_AllModels_AutoML_20200104_230354'
model = h2o.load_model(model_path)

df = h2o.upload_file("./datasets/allyears2k.csv")
splits= df.split_frame(ratios = [.8], seed = 123)
train = splits[0]
test = splits[1]

print("Model:")
print(model)

print("Model performance:")
perf = model.model_performance(test)
print(perf)

predicted = model.predict(test)
print(predicted.head())


