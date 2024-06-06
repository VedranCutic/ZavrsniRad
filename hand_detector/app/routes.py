from app import app
from flask import render_template, redirect, url_for, request
import subprocess
import os

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/webcam")
def webcam():
    return render_template("webcam.html", title="webcam")


@app.route("/webcam_trained")
def webcam_trained():
    return render_template("webcam_trained.html", title="webcam")


@app.route("/upload_trained")
def upload_trained():
    return render_template("upload_trained.html", title="upload")


@app.route("/upload")
def upload():
    return render_template("upload.html", title="upload")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "video" not in request.files:
        return "No video file provided"
    file = request.files["video"]
    if file.filename == "":
        return "No selected file"
    if file:
        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for("playback", filename=filename))


@app.route("/run-script")
def run_script():
    # This is where you can call your Python script
    subprocess.call(["python", "webcam.py", "--model", "pretrained"])
    return redirect(url_for("webcam"))


@app.route("/run-script_trained")
def run_script_trained():
    # This is where you can call your Python script
    subprocess.call(["python", "webcam.py", "--model", "trained"])
    return redirect(url_for("webcam_trained"))


@app.route("/playback/<filename>")
def playback(filename):
    video_url = url_for("static", filename=os.path.join("uploads", filename))
    print(video_url)
    return render_template("playback.html", video_url=video_url)
