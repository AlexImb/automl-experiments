import os
import openml
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
import sklearn.ensemble

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

from dotenv import load_dotenv
load_dotenv()

openml.config.apikey = os.getenv('OPENML_API_KEY')

task = openml.tasks.get_task(189354)
train_indices, test_indices = task.get_train_test_split_indices()

dataset = task.get_dataset()
X, y, categorical_mask, _ = dataset.get_data(target=task.target_name, dataset_format='array')

numeric_mask = [not x for x in categorical_mask]
print(categorical_mask)
print(numeric_mask)

numeric_transformer = Pipeline(steps=[
    ('numeric_imputer', SimpleImputer(strategy='median'))
])

categorical_transformer = Pipeline(steps=[
    ('categorical_inputer', SimpleImputer(strategy='constant')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

column_transformer = ColumnTransformer(transformers=[
        # ('num', numeric_transformer, numeric_mask),
        ('cat', categorical_transformer, categorical_mask)
])


clf = Pipeline(steps=[
    ('trasformer', column_transformer),
    ('estimator', sklearn.ensemble.GradientBoostingClassifier())
])


run = openml.runs.run_model_on_task(clf, task)

X_train = X[train_indices]
y_train = y[train_indices]
X_test = X[test_indices]
y_test = y[test_indices]

clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print("Accuracy score", sklearn.metrics.accuracy_score(y_test, predictions))
print("AUC", sklearn.metrics.auc(y_test, predictions))

run = run.publish()
print(run)