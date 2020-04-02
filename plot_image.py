import numpy as np
import matplotlib.pyplot as plt

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def plot_image(predictions_array, img):
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img)
    predicted_label = np.argmax(predictions_array)
    plt.xlabel("{} {:2.2f}% ".format(class_names[predicted_label],100*np.max(predictions_array)))

def plot_value_array(predictions_array):
    plt.grid(False)
    plt.xticks(range(10), class_names, rotation=45)
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)
    thisplot[predicted_label].set_color('red')

# def plot_prediction(predictions_array, img, data, filename):
#     plt.figure(figsize=(18, 6))
#     plt.subplot(1, 3, 1)
#     plot_image(predictions_array, img)
#     plt.subplot(1, 3, 2)
#     plt.figure()
#     plt.imshow(data)
#     plt.subplot(1, 3, 3)
#     plot_value_array(predictions_array)
#     plt.savefig('./temp/' + filename.rsplit('.', 1)[0].lower() + '.jpg')