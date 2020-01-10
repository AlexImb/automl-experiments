import os
import openml
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
import autosklearn.classification

from dotenv import load_dotenv
load_dotenv()

openml.config.apikey = os.getenv('OPENML_API_KEY')
print(openml.config.apikey)

task = openml.tasks.get_task(189354)
train_indices, test_indices = task.get_train_test_split_indices()
X, y = task.get_X_and_y()

X_train = X[train_indices]
y_train = y[train_indices]
X_test = X[test_indices]
y_test = y[test_indices]

dataset = task.get_dataset()
_, _, categorical_indicator, _ = dataset.get_data(target=task.target_name)

# Create feature type list from openml.org indicator and run autosklearn
feat_type = ['Categorical' if ci else 'Numerical' for ci in categorical_indicator]

cls = autosklearn.classification.AutoSklearnClassifier(
    time_left_for_this_task=120,
    per_run_time_limit=30,
)
cls.fit(X_train, y_train, feat_type=feat_type)

predictions = cls.predict(X_test)
print("Accuracy score", sklearn.metrics.accuracy_score(y_test, predictions))