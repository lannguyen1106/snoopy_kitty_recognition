import numpy as np
import tensorflow as tf
from flask import Flask, escape, render_template, request

app = Flask(__name__)

@app.route("/")
def main():
     return render_template("home.html")
