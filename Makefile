start-h2o:
	java -jar venv/lib/python3.7/site-packages/h2o/backend/bin/h2o.jar
train-h2o: 
	python training/h2o-train.py
predict-h2o:
	python prediction/h2o-predict.py
evaluate-stream:
	@echo 'Simulate'