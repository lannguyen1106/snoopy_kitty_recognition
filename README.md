# Snoopy Kitty Prediction Machine using Tensorflow

![](https://i.imgur.com/3aEyYcR.png)

A website application written in python Flask to predict dog and cat from users' uploaded images. This web application will use a trained model using Tensorflow 2.0-beta1 to predict the images.

## Web Application Features
* Upload image using AJAX technique.
* Predict cat or dog from uploaded images.
* Predict correction: allow users to select the correct object and save the information to the database. By doing this, we will be able to collect more data to improve our model accuracy in the future.

## Requirements
* Python 3
* Tensorflow 2.0.0-beta1
* Postgres database

## Installation

**Install flask**
`pip install Flask`

**Install psycopg2**
`pip install psycopg2`

**Install tensorflow 2.0beta1
`pip install tensorflow==2.0.0-beta1`

**Install Postgres database**
Please go to this website to install Postgres [https://www.postgresql.org/](https://www.postgresql.org/)

**Configure the database connection**
1. After installing Postgres database, please create a database named **snoopy_kitty**. 
2. Open **db_init.py** file and fill in your database information.

![](https://i.imgur.com/XWE6Pll.png)


## Our Dataset
The datasets contain 25,000 dogs & cats labeled images and 12,500 test images.

We splitted the train datasets to 20,000 images for training and 5,000 images for validating.

## How we train our model
We experiment 2 training strategies:
* Convolutional Neuron Network
* Transfer Learning using **MobileNet V2**, a model developed at Google and pre-trained on the ImageNet dataset.

### Our CNN Outlined Map
![](https://i.imgur.com/vhJlKzN.jpg)


## Model Accuracy
We achieved **91% validation accuracy** with our CNN model and **97.44% validation accuracy** with our transfer learing model. Therefore, we use our transfer learning model for the prediction engine.

![](https://i.imgur.com/1E7J7PD.png)

