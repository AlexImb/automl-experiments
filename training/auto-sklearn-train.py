import autosklearn.classification
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics

import pandas as pd
import numpy as np

df = pd.read_csv("./datasets/allyears2k.csv", low_memory=False)

df["Year"]= df["Year"].astype('category')
df["Month"]= df["Month"].astype('category')
df["DayOfWeek"] = df["DayOfWeek"].astype('category')
df["Cancelled"] = df["Cancelled"].astype('category')
df['FlightNum'] = df['FlightNum'].astype('category')
df['Origin'] = df['Origin'].astype('category')
df['Dest'] = df['Dest'].astype('category')
df['IsDepDelayed'] = df['Dest'].astype('category')

print(df.dtypes)

predictors = ["Origin", "Dest", "Year", "UniqueCarrier", "DayOfWeek", "Month", "Distance", "FlightNum"]
target = 'IsDepDelayed'

y = df.pop(target)
X = df[predictors]

X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, random_state=1)
automl = autosklearn.classification.AutoSklearnClassifier()

automl.fit(X_train, y_train)

y_hat = automl.predict(X_test)
print("Score", sklearn.metrics.accuracy_score(y_test, y_hat))