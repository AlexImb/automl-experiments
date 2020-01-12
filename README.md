# AutoML Experiments

A collection of AutoML experiments than can be executed in Docker and using Kafka as data source

## Running instructions

### Requirements

Required:
- Docker

Strongly recommended:
- Docker Compose
- Make

Usefull:
- kafkacat


### Starting the containers

All containers at once
```bash
make up
```

Individual containers:
```bash
docker-compose up auto-sklearn zookeeper broker
```

### Publishing a dataset to Kafka

OpenML dataset: 

```bash
make publish-openml-dataset
```

For any other dataset: 

```bash
cat ./datasets/covtype.csv | kafkacat -P -b localhost -t covtype   
```

### Running an experiment


```bash
make train-sklearn-batch
```

Or directly using Docker Compose

```bash
docker-compose exec auto-sklearn python training/sklearn-batch.py
```

Alternatively, you can run a single container using only Docker run.

### Opening Jupyter/JupyterLab

Find the right port for the experiment/service in the `docker-compose.yml`

Navigate to: `localhost:<port>`, for example: `localhost:8888`

Get the Jupyter token by running 

```bash
docker-compose logs <service_name>
```

For example: 

```bash
docker-compose logs auto-sklearn
```

Copy the token and use it to login in Jupyter.

## Development instructions

For developing the experiments it is useful to have the dependencies installed locally
in a `virtualenv`. It helps IDEs and linters to provide usefull information.

- Create and activate a `virtualenv`
- Install some or all dependencies from `dev-requirements.txt`

```bash
pip install -r dev-requirements.txt
```