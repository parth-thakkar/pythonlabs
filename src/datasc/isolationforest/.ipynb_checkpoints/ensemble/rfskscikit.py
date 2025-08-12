from sklearn.datasets import make_moons
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

X, y = make_moons(n_samples=500, noise=0.30, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

voting_clf = VotingClassifier(
    estimators=[
        ('lr', LogisticRegression(random_state=42)),
        ('rf', RandomForestClassifier(random_state=42)),
        ('svc', SVC(random_state=42))
    ]
)

voting_clf.fit(X_train, y_train)
print(voting_clf.estimators_)
print(voting_clf.estimators)
print(type(X_test))
print(X_test.ndim)
print(X_test)
print(y_test)

for name, clf in voting_clf.named_estimators_.items():
    print(name,"=", clf.__class__.__name__ , ",",clf.score(X_test, y_test))

for name, clf in voting_clf.named_estimators_.items():
    print(f"{name}: {clf.score(X_test, y_test):.2f}")