import numpy as np
import base64
import os
import logging
import re
import tensorflow as tf
from flask import Flask, escape, render_template, request, send_from_directory, redirect
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Jody Thai'

toolbar = DebugToolbarExtension(app)

dropzone = Dropzone(app)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

model = tf.keras.models.load_model("static/models/my_model.h5")

def parse_image(imgData):
  logging.info(imgData)
  imgstr = re.search(b"base64,(.*)", imgData).group(1)
  img_decode = base64.decodebytes(imgstr)
  with open("output.jpg", "wb") as file:
      file.write(img_decode)
  return img_decode

@app.route('/', methods=['GET', 'POST'])
def main():
  # list to hold our uploaded image urls
  file_urls = []
  
  if request.method == 'POST':
    file_obj = request.files
    # for f in file_obj:
    file = request.files.get(file_obj)

    img_raw = parse_image(request.get_data())
    
    # save the file with to our photos folder
    # filename = photos.save(
    #   file,
    #   name=file.filename    
    # )               
    # append image urls
    # file_urls.append(photos.url(filename))

    # Predict
    image = tf.image.decode_jpeg(img_raw, channels=1)
    image = tf.image.resize(image, [28, 28])
    image = (255 - image) / 255.0  # normalize to [0,1] range
    image = tf.reshape(image, (1, 28, 28, 1))

    probabilites = model.predict(image)
    prediction = np.argmax(probabilites, axis=1)

    return str(prediction)
        
    return "uploading..."

  return render_template('home.html')

if __name__ == '__main__':
  app.run()