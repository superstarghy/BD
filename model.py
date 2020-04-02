# An Introductory Course About Tensorflow
# An Example of Basic Classification, Machine learning
# Source: https://tensorflow.google.cn/tutorials/keras/classification

from __future__ import absolute_import, division, print_function, unicode_literals

# TensorFlow and keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import os
import numpy as np
import matplotlib.pyplot as plt

# Load the Fashion MINST data
# The Data returns four NumPy arrays, 6w images for training set & 1w for testing set
# images are 28*28 numpy arrays(pixel value: 0~255)
(train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()
# Classification
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Preprocess the data, Scale pixel values to a range of 0 to 1
train_images = train_images / 255.0
test_images = test_images / 255.0

# Build the Model
# Set up the layers
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10)
])
# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model
# Feed the training data to the model, set epoches=10
model.fit(train_images,
            train_labels,
            epochs=15
            )
# Evaluate accuracy
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

# Make predictions
# Softmax convert the logits, the linear outputs of the model, to probabilities
probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_images)
print(predictions[0])
# argmax from numpy choose the highest confidence value
pt = np.argmax(predictions[0])
print(class_names[pt])

# save the entire model
model.save('my_model.h5')

# use the model
img = test_images[8]
plt.figure()
plt.imshow(img)
plt.show()
img = (np.expand_dims(test_images[8],0))
predictions_single = probability_model.predict(img)
print(predictions_single)
pt = np.argmax(predictions[0])
print(class_names[pt])