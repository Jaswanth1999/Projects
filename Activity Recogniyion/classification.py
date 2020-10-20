# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 12:36:08 2020

@author: jaswa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import itertools


Data = pd.read_csv("Data.csv")
Data = Data.values
X = Data[:,1:-1]
y = Data[:,-1]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
slice = X_train.shape[1]



from keras.utils import to_categorical

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

X_train = X_train.reshape(X_train.shape[0],slice,1)
X_test = X_test.reshape(X_test.shape[0],slice,1)


from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten,MaxPooling1D
#create model
model = Sequential()
#add model layers
model.add(Conv1D(64, kernel_size=3, activation='relu', input_shape=(slice,1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(64, kernel_size=3,activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(32, kernel_size=3, activation='relu'))
model.add(Conv1D(32, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(20, activation='relu'))
model.add(Dense(4, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train,y_train, epochs=100, batch_size=32, verbose=0)
model.add
_, accuracy = model.evaluate(X_test, y_test, batch_size=32, verbose=0)
print(accuracy)

y_pred = model.predict(X_test)
matrix = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
print(matrix)
