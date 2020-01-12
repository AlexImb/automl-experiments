from skmultiflow.data import WaveformGenerator
from skmultiflow.trees import HoeffdingTree
from skmultiflow.meta import OzaBagging
from skmultiflow.evaluation import EvaluatePrequential
from kafka_stream import KafkaStream
from skmultiflow.data import FileStream

INPUT_TOPIC = 'elec_4'
stream = KafkaStream(INPUT_TOPIC, bootstrap_servers='localhost:9092')
# stream = KafkaStream(INPUT_TOPIC, bootstrap_servers='broker:29092')

# stream = FileStream('datasets/covtype.csv')

stream.prepare_for_use()

ht = HoeffdingTree()

evaluator = EvaluatePrequential(show_plot=True,
                                pretrain_size=200,
                                max_samples=3000,
                                output_file='results/multiflow.hoeff.csv')

evaluator.evaluate(stream=stream, model=[ht], model_names=['HT'])
