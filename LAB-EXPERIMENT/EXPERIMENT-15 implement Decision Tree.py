from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(
    criterion="entropy",
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Decision Tree Classification")
print("----------------------------")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nPredicted values:")
print(y_pred)

print("\nActual values:")
print(y_test)

print("\nAccuracy:", accuracy * 100, "%")
