from tpot import TPOTClassifier
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split as split

digits = load_digits()
X_train, X_test, y_train, y_test = split(digits.data, digits.target)

pipeline_optimizer = TPOTClassifier(generations=5, population_size=20, cv=5)
pipeline_optimizer.fit(X_train, y_train)
print(pipeline_optimizer.score(X_test, y_test))
pipeline_optimizer.export('../models/tpot_exported_pipeline.py')
