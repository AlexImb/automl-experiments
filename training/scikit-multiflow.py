from skmultiflow.data import FileStream
from skmultiflow.trees import HoeffdingTree
from skmultiflow.evaluation import EvaluatePrequential

stream = FileStream('datasets/elec.csv')
stream.prepare_for_use()

ht = HoeffdingTree()

evaluator = EvaluatePrequential(show_plot=False,
                                pretrain_size=20,
                                max_samples=500)

evaluator.evaluate(stream=stream, model=ht)