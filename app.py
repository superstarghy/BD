from __future__ import absolute_import, division, print_function, unicode_literals

# tensorflow
import tensorflow as tf
from tensorflow import keras

# flask
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import os
import matplotlib.pyplot as plt
import numpy as np
from plot_image import plot_value_array, plot_image
from PIL import Image
# # 读取文图像文件
# (train_images, train_labels), (test_images, test_labels) = keras.datasets.fashion_mnist.load_data()
def predicting(filename):
    # Classification
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    # 图像转化
    fp = './temp/' + filename
    img = Image.open(fp) # 打开图像，格式为RGB
    data = img.resize((28, 28)) # 缩放为28*28分辨率
    data = data.convert("L") # 转化为0~255像素值灰度图
    data = np.array(data)
    # 背景清空
    m = data[0][0]
    for i in range(28):
        for j in range(28):
            if abs(data[i][j] - m) < 5:
                data[i][j] = 0

    data = data / 255.0

    # 加载模型
    new_model = keras.models.load_model('my_model.h5')
    new_model = tf.keras.Sequential([new_model, tf.keras.layers.Softmax()])
    prediction = new_model.predict(np.expand_dims(data,0))
    predict_label = np.argmax(prediction[0])
    
    plt.figure(figsize=(24, 8))
    plt.subplot(1, 3, 1)
    plot_image(prediction[0], img)
    plt.subplot(1, 3, 2)
    plt.imshow(data * 255.0, cmap=plt.cm.binary)
    plt.subplot(1, 3, 3)
    plot_value_array(prediction[0])
    plt.savefig('./temp/' + filename.rsplit('.', 1)[0].lower() + '.jpg')

    return predict_label, class_names[predict_label]


UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# 新建flask类的实例
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查用户上传的文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <title>Upload new File</title>
    <h1>Upload A Fashion Minist Image</h1>
    <p>(Only images with <b>['png', 'jpg', 'jpeg', 'gif', 'bmp']</b> format are permitted)</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </html>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    predicting(filename)
    na = filename.rsplit('.', 1)[0].lower() + '.jpg'
    # return str(label) + "\n" + na
    return send_from_directory(app.config['UPLOAD_FOLDER'], na)
