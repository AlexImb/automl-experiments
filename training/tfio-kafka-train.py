import tensorflow as tf
import tensorflow_io.kafka as tfio
from tensorflow.keras import layers

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.boston_housing.load_data(
    path='boston_housing.npz',
    test_split=0.2,
    seed=13
)

model = tf.keras.models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(13,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

model.fit(x_train, y_train, epochs=120, batch_size=16, verbose=0)

loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)
print(loss_and_metrics)

# classes = model.predict(x_test, batch_size=128)

# tfio.write_kafka(
#     'bam',
#     'test_jupyter',
#     servers="localhost:9092"
# )

# kafka_ds = tfio.KafkaDataset(
#     'test_jupyter',
#     servers='localhost:9092',
#     group="tfio"
# )

# ds = kafka_ds.batch(
#     2,
#     drop_remainder=False
# )

# for data in ds:
#     print(data)