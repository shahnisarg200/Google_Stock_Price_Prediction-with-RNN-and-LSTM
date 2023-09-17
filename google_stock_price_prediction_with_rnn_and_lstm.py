# -*- coding: utf-8 -*-
"""Google Stock Price Prediction with RNN and LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lszJfFT9VgdsQFvp19RM7AiNmX-zzZ83
"""

!pip install tensorflow-gpu

import tensorflow as tf

print(tf.__version__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

training_data = pd.read_csv('/content/training_set.csv')

training_data.head()

training_data.tail()

training_data.info()

training_set = training_data.iloc[:, 1:2].values

training_set.shape, training_data.shape

# Apply Feature scaling - In RNN we use Normalization
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)

training_set_scaled

#Creating a data Structure with 60 timesteps and 1 output
x_train = []
y_train = []

for i in range(60, 1257):
  x_train.append(training_set_scaled[i-60:i,0])
  y_train.append(training_set_scaled[i,0])

#Converting x_train, y_train to numpy array
x_train, y_train = np.array(x_train), np.array(y_train)

x_train

y_train

x_train.shape

# Reshaping the dataset - RNN takes 3 dimensions instead of 2
x_train = x_train.reshape(1197,60,1)

x_train.shape

"""Building LSTM"""

# Define an object (inilitizing RNN)
model = tf.keras.models.Sequential()

#Add LSTM Layers - First layer
model.add(tf.keras.layers.LSTM(units = 60, activation = 'relu', return_sequences = True, input_shape=(60,1)))
# dropout layer
model.add(tf.keras.layers.Dropout(0.2))

#Second LSTM layer
model.add(tf.keras.layers.LSTM(units = 60, activation = 'relu', return_sequences = True))
# dropout layer
model.add(tf.keras.layers.Dropout(0.2))

#Third LSTM layer
model.add(tf.keras.layers.LSTM(units = 80, activation = 'relu', return_sequences = True))
# dropout layer
model.add(tf.keras.layers.Dropout(0.2))

#Fourth LSTM layer
model.add(tf.keras.layers.LSTM(units = 120, activation = 'relu'))
# dropout layer
model.add(tf.keras.layers.Dropout(0.2))

#Add output layer
model.add(tf.keras.layers.Dense(units=1))

model.summary()

#Compile the model
 model.compile(optimizer='adam', loss='mean_squared_error')

"""Training the Model"""

model.fit(x_train, y_train, batch_size=32, epochs=100)

"""Making Predictions"""

# getting the real stock prices of the month Nov 2019
test_data = pd.read_csv("/content/test_set.csv")

test_data.shape

test_data.info()

real_stock_price = test_data.iloc[:, 1:2].values

real_stock_price

real_stock_price.shape

#Getting Predicated stock prices for Nov 2019

#Concatination
dataset_total = pd.concat((training_data['Open'],test_data['Open']),axis=0)

#stock prices pf previous 60 days for each day of Nov 2019
inputs = dataset_total[len(dataset_total)-len(test_data)-60:].values

#reshape (Convert into numpy array)
inputs = inputs.reshape(-1,1)

#feature scaling
inputs = sc.transform(inputs)

#creating a test set
x_test = []
for i in range(60,80):
  x_test.append(inputs[i-60:i,0])

#convert to numpy array
x_test = np.array(x_test)

#convert into 3D
x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1], 1))

#getting predicted stock prices
predicted_stock_price = model.predict(x_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

print(predicted_stock_price[5]), print(real_stock_price[5])

"""Visualisation"""

plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock price')
plt.legend()
plt.show()

