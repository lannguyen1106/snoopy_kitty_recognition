import numpy as np
import base64
import os
import logging
import re
import sys
import tensorflow as tf
from werkzeug import secure_filename
from flask import Flask, flash, escape, render_template, request, send_from_directory, redirect, session, url_for, jsonify
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Jody Thai'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

IMAGE_WIDTH = 120
IMAGE_HEIGHT = 120

# toolbar = DebugToolbarExtension(app)

# dropzone = Dropzone(app)

# Dropzone settings
# app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
# app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
# app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
# app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

# app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)
# patch_request_class(app)

model = tf.keras.models.load_model("static/models/my_model_tl_sigmoid_acc95.h5")

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def main():
  return render_template('home.html')

@app.route('/upload-image/', methods=['GET', 'POST'])
def upload_image():

  prediction_probs = ''
  label = ''
  
  if request.method == 'POST':

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
      upload_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(upload_file_path)
      # return redirect(url_for('uploaded_file', filename=filename))

      # img_raw = parse_image(request.get_data())
      image_raw = tf.io.read_file(upload_file_path)
      image = tf.image.decode_jpeg(image_raw, channels=3)
      image = tf.image.resize(image, [IMAGE_HEIGHT, IMAGE_WIDTH])
      image = (255 - image) / 255.0  # normalize to [0,1] range
      image = tf.reshape(image, (1, IMAGE_HEIGHT, IMAGE_WIDTH, 3))

      probs = model.predict(image)
      print('probs\n', file=sys.stdout)
      print(probs, file=sys.stdout)
      
      prediction = probs[0][0]
      print('prediction\n', file=sys.stdout)
      print(prediction, file=sys.stdout)
      
      label = "Dog" if prediction >= 0.5 else "Cat"
      
      prediction_probs = prediction if prediction >= 0.5 else 1 - prediction
      prediction_probs = round((prediction_probs * 100), 2)
      print('prediction_probs\n', file=sys.stdout)
      print(prediction_probs, file=sys.stdout)
      # label = "Dog" if probs >= 0.5 else "Cat"
      # prediction = np.argmax(probabilites, axis=1)
      # prediction_probs = probs if probs >= 0.5 else 1 - probs
      # prediction_probs = round((prediction_probs[0][0] * 100), 2)

      predict_image = base64.b64encode(image_raw)
  
  return jsonify({'label': label, 'probs': str(prediction_probs)})

if __name__ == '__main__':
  app.run()