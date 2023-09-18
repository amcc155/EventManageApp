# Copyright © 2023, Indiana University
# BSD 3-Clause License

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
