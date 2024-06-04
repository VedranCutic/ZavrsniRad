from app import app
from flask import render_template, redirect, url_for
import subprocess


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/webcam")
def webcam():
    return render_template("webcam.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/run-script")
def run_script():
    # This is where you can call your Python script
    subprocess.call(["python", "webcam.py"])
    return redirect(url_for("index"))
