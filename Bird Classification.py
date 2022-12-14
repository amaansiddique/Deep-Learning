# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/mohanrajmit/Bird-Classification-using-CNN/blob/master/bird_neuralnet.ipynb
"""

from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization

# Load data set
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# CIFAR10 has ten types of images labeled from 0 to 9. We only care about birds, which are labeled as class #2.
# So we'll cheat and change the Y values. Instead of each class being labeled from 0 to 9, we'll set it to True
# if it's a bird and False if it's not a bird.
y_train = (y_train == 2).astype(int)
y_test = (y_test == 2).astype(int)

x_train = x_train.reshape(50000,3072)
x_test = x_test.reshape(10000,3072)

# Normalize image data (pixel values from 0 to 255) to the 0-to-1 range
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

print(x_test.shape)
print(x_train.shape)

from keras.layers import Input
from keras.models import Model
from keras.models import Sequential

model = Sequential()
model.add(Dense(1024, input_dim=3072,activation='relu'))
model.add(Dense(512, activation="relu"))
model.add(Dense(256, activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.summary()

model.compile(loss='binary_crossentropy',optimizer="adam",metrics=['accuracy'])

model.fit(x_train,y_train,
          batch_size=32,
          epochs=10,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# Save the trained model to a file so we can use it to make predictions later
model.save("bird_model.h5")

from sklearn.metrics import confusion_matrix, classification_report
from keras.models import load_model

# Load the model we trained
model = load_model('bird_model.h5')
predictions = model.predict(x_test, batch_size=32, verbose=1)

# If the model is more than 50% sure the object is a bird, call it a bird.
# Otherwise, call it "not a bird".
predictions = predictions > 0.5

# Calculate how many mis-classifications the model makes
tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()
print(f"True Positives: {tp}")
print(f"True Negatives: {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")

# Calculate Precision and Recall for each class
report = classification_report(y_test, predictions)
print(report)

import numpy as np
import matplotlib.pyplot as plt
import cv2
img=cv2.imread("/content/1.png")
img2=cv2.resize(img, (32, 32),interpolation=cv2.INTER_AREA)
img1=img2.flatten()
img1=img1.reshape(1,-1)
# insert a new axis along the row
#sample_test_image = x_test[100]
#b = np.expand_dims(img2, axis=0)
res=model.predict(img1)
#print(label_name[int(res)])

plt.imshow(img)
print(res)
if res > 0.5:
  print("bird")
else:
  print("not bird")

