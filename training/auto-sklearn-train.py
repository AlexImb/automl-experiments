import os
import openml
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
import autosklearn.classification

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

from dotenv import load_dotenv
load_dotenv()

openml.config.apikey = os.getenv('OPENML_API_KEY')

task = openml.tasks.get_task(7592)
train_indices, test_indices = task.get_train_test_split_indices()
X, y = task.get_X_and_y()

dataset = task.get_dataset()
_, _, categorical_mask, _ = dataset.get_data(target=task.target_name)

numeric_mask = [not x for x in categorical_mask]
print(categorical_mask)
print(numeric_mask)

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

column_transformer = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_mask),
        ('cat', categorical_transformer, categorical_mask)
])

X = column_transformer.fit_transform(X)

X_train = X[train_indices]
y_train = y[train_indices]
X_test = X[test_indices]
y_test = y[test_indices]

cls = autosklearn.classification.AutoSklearnClassifier(
    time_left_for_this_task=120,
    per_run_time_limit=30,
)
cls.fit(X_train, y_train)

predictions = cls.predict(X_test)
print("Accuracy score", sklearn.metrics.accuracy_score(y_test, predictions))
