from skmultiflow.trees import HoeffdingTree
from skmultiflow.evaluation import EvaluatePrequential
from kafka_stream import KafkaStream

INPUT_TOPIC = 'covtype'
stream = KafkaStream(INPUT_TOPIC, bootstrap_servers='broker:29092')

stream.prepare_for_use()

ht = HoeffdingTree()

evaluator = EvaluatePrequential(show_plot=False,
                                pretrain_size=200,
                                max_samples=3000,
                                output_file='results/multiflow.hoeff.csv')

evaluator.evaluate(stream=stream, model=[ht], model_names=['HT'])
