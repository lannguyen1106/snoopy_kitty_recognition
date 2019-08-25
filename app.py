import numpy as np
import base64
import os
import logging
import re
import sys
import datetime
import db_init as db
import tensorflow as tf
from werkzeug import secure_filename
from flask import Flask, flash, escape, render_template, request, send_from_directory, redirect, session, url_for, jsonify

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Jody Thai'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# load the trained model
model = tf.keras.models.load_model("static/models/my_model_tl_sigmoid_rmsprop_acc9755.h5")

# change these two values to match the image width and height in the trained model
IMAGE_WIDTH = 165
IMAGE_HEIGHT = 165

def allowed_file(filename):
  """
  Security purpose: this function will check if the uploaded file extension is allowed or not
  """
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Homepage
@app.route('/')
def main():
  return render_template('home.html')

# Handle image upload
@app.route('/upload-image/', methods=['GET', 'POST'])
def upload_image():
  """
  This function handle the upload image request from the frond end user interface
  """
  prediction_probs = ''
  label = ''
  
  if request.method == 'POST':
    
    # check if the file is not appropriate
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)

    # retrieve the image from the ajax request
    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      return jsonify({'label': 'No file selected', 'probs': ''})

    if file and allowed_file(file.filename):
      # security stuff
      filename = secure_filename(file.filename)
      # get the full file path
      upload_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      # save the image to our uploads folder
      file.save(upload_file_path)
      
      # preprocess the image for predicting
      image_raw = tf.io.read_file(upload_file_path)
      image = tf.image.decode_jpeg(image_raw, channels=3)
      image = tf.image.resize(image, [IMAGE_HEIGHT, IMAGE_WIDTH])
      image = (255 - image) / 255.0  # normalize to [0,1] range
      image = tf.reshape(image, (1, IMAGE_HEIGHT, IMAGE_WIDTH, 3))

      # predict the image
      probs = model.predict(image)
      prediction = probs[0][0]

      # make the label from precision
      label = "Dog" if prediction >= 0.5 else "Cat"
      
      # change prediction probability to percentage format
      prediction_probs = prediction if prediction >= 0.5 else 1 - prediction
      prediction_probs = round((prediction_probs * 100), 2)
      # print('prediction_probs\n', file=sys.stdout)
      # print(prediction_probs, file=sys.stdout)
  
  return jsonify({'label': label, 'probs': str(prediction_probs), 'upload_file_path': upload_file_path})

# Handle predict correction
@app.route('/predict-correction/', methods=['POST'])
def predict_correction():

  results = {}

  try:
    # get data from the UI form ajax submission
    data_upload_file_path = request.form['upload-file-path']
    data_correction_label = request.form['correction-label']

    if data_upload_file_path != '':
      created_on = datetime.datetime.now()

      # create database table first
      db.create_tables()

      # insert into database
      db.insert_row((data_upload_file_path, data_correction_label, created_on), 'predict_correction')
      results['status'] = 'success'
      results['message'] = 'Thank you for your correction!!!'
  except Exception as error:
    results['status'] = 'exception'
    results['message'] = 'ERROR: ' + error

  return jsonify(results)

if __name__ == '__main__':
  app.run()