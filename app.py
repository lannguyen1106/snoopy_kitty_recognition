import numpy as np
import tensorflow as tf
from flask import Flask, escape, render_template, request

app = Flask(__name__)

if __name__ == "__main__":
    app.run()


@app.route("/")
def hello():
    name = request.args.get("name", "Duong")
    return f"Hello, {escape(name)}!"
