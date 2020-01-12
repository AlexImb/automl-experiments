from skmultiflow.data import FileStream, WaveformGenerator
from skmultiflow.evaluation.evaluate_stream_gen_speed import EvaluateStreamGenerationSpeed
from skmultiflow.meta import OzaBagging
from skmultiflow.trees import HoeffdingTree

from kafka_stream import KafkaStream

INPUT_TOPIC = 'elec_4'
# stream = KafkaStream(INPUT_TOPIC, bootstrap_servers='localhost:9092')
stream = KafkaStream(INPUT_TOPIC, bootstrap_servers='broker:29092')

# stream = FileStream('datasets/elec.csv')

stream.prepare_for_use()

evaluator = EvaluateStreamGenerationSpeed(10000, float("inf"), None, 10)

stream = evaluator.evaluate(stream)
