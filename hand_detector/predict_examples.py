from ultralyticsplus import YOLO
import torch
import argparse
import shutil
import os


files = os.listdir("../primjeri")

# PRETRAINED
# Set device to CPU explicitly
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load model and move it to the correct device
model = YOLO("lewiswatson/yolov8x-tuned-hand-gestures").to(device)
model.model.names[15] = "back-fist"
model.model.names[16] = "front-fist"
model.model.names[18] = "two"
model.model.names[19] = "open-palm"
model.model.names[20] = "three"
model.model.names[8] = "one"

for file in files:
    file_path = f"../primjeri/{file}"
    model.predict(file_path, save=True, project="primjeri_predicted_lewis", name=file)

# TRAINED
model = YOLO("best.pt")
model.model.names[0] = "palm"
model.model.names[1] = "palm"

for file in files:
    file_path = f"../primjeri/{file}"
    model.predict(file_path, save=True, project="primjeri_predicted", name=file)
