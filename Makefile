start-h2o:
	java -jar venv/lib/python3.7/site-packages/h2o/backend/bin/h2o.jar
train-gbm-h2o: 
	python training/h2o-gbm-train.py
train-automl-h2o: 
	python training/h2o-automl-train.py
predict-h2o:
	python prediction/h2o-predict.py
predict-stream:
	python prediction/h2o-kafka-predict.py