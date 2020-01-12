from skmultiflow.evaluation.evaluate_stream_gen_speed import EvaluateStreamGenerationSpeed
from kafka_stream import KafkaStream

INPUT_TOPIC = 'elec_4'

stream = KafkaStream(INPUT_TOPIC, bootstrap_servers='broker:29092')

stream.prepare_for_use()

evaluator = EvaluateStreamGenerationSpeed(10000, float("inf"), None, 10)

stream = evaluator.evaluate(stream)
