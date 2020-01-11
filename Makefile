# Start all containers: experiments + Kafka Cluster
up:
	docker-compose up

# Stop and remove all containers
down:
	docker-compose down


# Publish OpenML Dataset to Kafka
publish-dataset: 
	docker-compose exec scikit-multiflow python producers/openml-kafka.py


# Scikit-learn
train-sklearn-batch: 
	docker-compose exec auto-sklearn python training/sklearn-batch.py
train-sklearn-online: 
	docker-compose exec auto-sklearn python training/sklearn-online.py


# Scikit-multiflow
train-scikit-multiflow:
	docker-compose exec scikit-multiflow python training/scikit-multiflow.py


# Auto-sklearn
train-auto-sklearn: 
	docker-compose exec auto-sklearn python training/auto-sklearn-train.py

# Spark Streaming
train-spark: 
	docker-compose exec h2o python training/spark-train.py

# H2O.ai
train-h2o-gbm: 
	docker-compose exec h2o python training/h2o-gbm-train.py
train-h2o-automl: 
	docker-compose exec h2o python training/h2o-automl-train.py
predict-h2o-batch:
	docker-compose exec h2o python prediction/h2o-predict.py
predict-h2o-stream:
	docker-compose exec h2o python prediction/h2o-kafka-predict.py

# Tensorflow IO
train-tf-kafka: 
	python training/tfio-kafka-train.py

# TPOT
train-tpot: 
	python training/tpot-train.py