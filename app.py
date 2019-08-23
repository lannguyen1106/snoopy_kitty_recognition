import numpy as np
import os
import re
import tensorflow as tf
from flask import Flask, escape, render_template, request, send_from_directory

app = Flask(__name__)

def parse_image(imgData):
    imgstr = re.search(b"base64,(.*)", imgData).group(1)
    img_decode = base64.decodebytes(imgstr)
    with open("output.jpg", "wb") as file:
        file.write(img_decode)
    return img_decode

@app.route("/")
def main():
     return render_template("home.html")

@app.route("/upload", methods = ['GET', 'POST'])
def upload_file():
    # img_raw = parse_image(request.get_data())

    if request.method == 'POST':
      uploaded_file = request.files['file']

    # image = tf.image.decode_jpeg(img_raw, channels=1)
    # image = tf.image.resize(image, [28, 28])
    # image = (255 - image) / 255.0  # normalize to [0,1] range
    # image = tf.reshape(image, (1, 28, 28, 1))

    # probabilites = model.predict(image)
    # prediction = np.argmax(probabilites, axis=1)
    # return str(prediction)

    return uploaded_file

if __name__ == '__main__':
  app.run(debug = True)