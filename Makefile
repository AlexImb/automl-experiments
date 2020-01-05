# H2O.ai
start-h2o:
	java -jar venv/lib/python3.7/site-packages/h2o/backend/bin/h2o.jar
train-h2o-gbm: 
	python training/h2o-gbm-train.py
train-h2o-automl: 
	python training/h2o-automl-train.py
predict-h2o-batch:
	python prediction/h2o-predict.py
predict-h2o-stream:
	python prediction/h2o-kafka-predict.py

# Tensorflow IO
train-tf-kafka: 
	python training/tfio-kafka-train.py

# Auto-sklearn
train-auto-sklearn: 
	python training/auto-sklearn-train.py

# TPOT
train-tpot: 
	python training/tpot-train.py