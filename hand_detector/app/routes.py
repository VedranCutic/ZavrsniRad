from app import app
from flask import render_template, redirect, url_for, request, send_from_directory
import subprocess
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "../uploads")
PREDICTED_FOLDER = os.path.join(BASE_DIR, "../runs/detect/predict")
DELETE_FOLDER = os.path.join(BASE_DIR, "../runs/detect")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PREDICTED_FOLDER"] = PREDICTED_FOLDER


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/webcam")
def webcam():
    return render_template("webcam.html", title="Webcam")


@app.route("/webcam_trained")
def webcam_trained():
    return render_template("webcam_trained.html", title="Webcam")


@app.route("/upload_trained")
def upload_trained():
    filename = request.args.get("filename")
    predicted = request.args.get("predicted")
    return render_template(
        "upload_trained.html", title="Upload", filename=filename, predicted=predicted
    )


@app.route("/upload_trained", methods=["POST"])
def upload_trained_file():
    if "video" not in request.files:
        return "No video file provided"
    file = request.files["video"]
    if file.filename == "":
        return "No selected file"
    if file:
        filename_v = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename_v))
        return redirect(url_for("upload_trained", title="Upload", filename=filename_v))


@app.route("/upload")
def upload():
    filename = request.args.get("filename")
    predicted = request.args.get("predicted")
    return render_template(
        "upload.html", title="Upload", filename=filename, predicted=predicted
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if "video" not in request.files:
        return "No video file provided"
    file = request.files["video"]
    if file.filename == "":
        return "No selected file"
    if file:
        filename_v = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename_v))
        return redirect(url_for("upload", title="Upload", filename=filename_v))


@app.route("/predict_upload/<filename>")
def predict_upload(filename):
    # Execute the upload.py script with the provided filename
    filename_v = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    subprocess.run(
        ["python", "upload.py", "--model", "pretrained", "--file", filename_v]
    )
    return redirect(url_for("upload", filename=filename, predicted=filename))


@app.route("/predict_upload_trained/<filename>")
def predict_upload_trained(filename):
    # Execute the upload.py script with the provided filename
    filename_v = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    subprocess.run(["python", "upload.py", "--model", "trained", "--file", filename_v])
    return redirect(url_for("upload_trained", filename=filename, predicted=filename))


@app.route("/run-script")
def start_webcam():
    # This is where you can call your Python script
    subprocess.call(["python", "webcam.py", "--model", "pretrained"])
    return redirect(url_for("webcam"))


@app.route("/run-script_trained")
def start_webcam_trained():
    # This is where you can call your Python script
    subprocess.call(["python", "webcam.py", "--model", "trained"])
    return redirect(url_for("webcam_trained"))


@app.route("/playback/<filename>")
def playback(filename):
    video_url = url_for("static", filename=os.path.join("uploads", filename))
    return render_template("playback.html", video_url=video_url)


@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(
        directory=app.config["UPLOAD_FOLDER"], path=filename, as_attachment=True
    )


@app.route("/download_predicted/<filename>", methods=["GET"])
def download_predicted(filename):
    filename = filename.split(".")
    if filename[1] == "mp4":
        filename = f"{filename[0]}.avi"
    elif filename[1] == "jpg":
        filename = f"{filename[0]}.jpg"
    elif filename[1] == "jpeg":
        filename = f"{filename[0]}.jpeg"
    return send_from_directory(
        directory=app.config["PREDICTED_FOLDER"], path=filename, as_attachment=True
    )
