import numpy as np
import base64
import os
import logging
import re
import tensorflow as tf
from flask import Flask, flash, escape, render_template, request, send_from_directory, redirect, session, url_for
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Jody Thai'

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

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

model = tf.keras.models.load_model("static/models/my_model.h5")

def parse_image(imgData):
  imgstr = re.search(b"base64,(.*)", imgData).group(1)
  img_decode = base64.decodebytes(imgstr)
  with open("output.jpg", "wb") as file:
      file.write(img_decode)
  return img_decode

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
  # # set session for image results
  # if "file_urls" not in session:
  #     session['file_urls'] = []
  # # list to hold our uploaded image urls
  # file_urls = session['file_urls']

  # if request.method == 'POST':
  #   file_obj = request.files[0]

  #   # for f in file_obj:
  #   file = request.files.get(file_obj)
    
  #   # save the file with to our photos folder
  #   filename = photos.save(
  #       file,
  #       name=file.filename
  #   )

  #   # append image urls
  #   file_urls.append(photos.url(filename))

  #   image = file.save(image)

  # Predict
  # image = tf.image.decode_jpeg(image, channels=1)
  # image = tf.image.resize(image, [28, 28])
  # image = (255 - image) / 255.0 # normalize to [0,1] range
  # image = tf.reshape(image, (1, 28, 28, 1))

  # probabilites = model.predict(image)
  # prediction = np.argmax(probabilites, axis=1)

  # return str(prediction)

  return render_template('home.html')

@app.route('/upload-image/', methods=['GET', 'POST'])
def upload_image():
  prediction = ''

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
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      # return redirect(url_for('uploaded_file', filename=filename))

      # img_raw = parse_image(request.get_data())

      image = tf.image.decode_jpeg(file, channels=1)
      image = tf.image.resize(image, [28, 28])
      image = (255 - image) / 255.0  # normalize to [0,1] range
      image = tf.reshape(image, (1, 28, 28, 1))

      probabilites = model.predict(image)
      prediction = np.argmax(probabilites, axis=1)
  
  return str(prediction)

if __name__ == '__main__':
  app.run()