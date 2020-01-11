import os
from dotenv import load_dotenv
import openml

import autosklearn.classification
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Load env variables from .env file
load_dotenv()

# Load from the environment
OPENML_API_KEY = os.getenv('OPENML_API_KEY')
OPENML_PUBLISH = os.getenv('OPENML_PUBLISH', False) == 'True'

openml.config.apikey = OPENML_API_KEY
# Adult: https://www.openml.org/t/7592
task = openml.tasks.get_task(7592)

X, y, categorical_mask, _ = task.get_dataset().get_data(
                                target=task.target_name,
                                dataset_format='array')

numeric_mask = [not x for x in categorical_mask]

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

auto_estimator = autosklearn.classification.AutoSklearnClassifier(
    time_left_for_this_task=120,
    per_run_time_limit=30,
)

estimator = Pipeline(steps=[
    ('trasformer', column_transformer),
    ('estimator', auto_estimator)
])

cv_folds = 3
scoring = ['accuracy', 'roc_auc']
results = cross_validate(estimator, X, y, cv=cv_folds, scoring=scoring)

print(f'Metrics for {cv_folds} cross-validation: ')
print('Accuracy: ', results['test_accuracy'])
print('AUC: ', results['test_roc_auc'])

if OPENML_PUBLISH:
    run = openml.runs.run_model_on_task(estimator, task)
    run = run.publish()
    print('Results published to OpenML', run)
