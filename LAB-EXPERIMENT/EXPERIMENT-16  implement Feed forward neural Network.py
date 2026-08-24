import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Input data
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
y = np.array([
    [0],
    [1],
    [1],
    [0]
])
model = Sequential()

model.add(Dense(8, input_dim=2, activation='relu'))

model.add(Dense(1, activation='sigmoid'))

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model.fit(X, y, epochs=1000, verbose=0)
predictions = model.predict(X)

print("Feed Forward Neural Network")
print("---------------------------")
for i in range(len(X)):
    result = 1 if predictions[i][0] >= 0.5 else 0

    print(
        "Input:", X[i],
        "Predicted:", result,
        "Actual:", y[i][0]
    )
