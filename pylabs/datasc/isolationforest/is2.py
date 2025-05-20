from sklearn.ensemble import IsolationForest
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.utils import resample
import pandas as pd



def test1():
    breast_cancer = load_breast_cancer()
    df = pd.DataFrame(data=breast_cancer.data, columns=breast_cancer.feature_names)
    df["benign"] = breast_cancer.target
    df.head()

    majority_df = df[df["benign"] == 1]
    minority_df = df[df["benign"] == 0]
    minority_downsampled_df = resample(minority_df, replace=True, n_samples=30, random_state=42)
    downsampled_df = pd.concat([majority_df, minority_downsampled_df])

    y = downsampled_df["benign"]
    X = downsampled_df.drop("benign", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = IsolationForest(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred = [1 if i == 1 else 0 for i in y_pred]
    # y_pred[y_pred == -1] = 0
    confusion_matrix(y_test, y_pred)



    # https://medium.com/@corymaklin/isolation-forest-799fceacdda4