from ultralyticsplus import YOLO
import torch
import argparse
import shutil


def arguments_parser():
    parser = argparse.ArgumentParser(description="arguments parser")
    parser.add_argument("--model")
    parser.add_argument("--file")
    args = parser.parse_args()
    return args


args = arguments_parser()
if args.model == "pretrained":
    model = YOLO("lewis.pt")

    model.model.names[15] = "back-fist"
    model.model.names[16] = "front-fist"
    model.model.names[18] = "two"
    model.model.names[19] = "open-palm"
    model.model.names[20] = "three"
    model.model.names[8] = "one"

elif args.model == "trained":
    model = YOLO("best.pt")
    model.model.names[0] = "palm"
    model.model.names[1] = "palm"

directory_to_delete = "runs/detect/predict"

try:
    shutil.rmtree(directory_to_delete)
    print(
        f"Directory '{directory_to_delete}' and all its contents are successfully deleted."
    )
except OSError as e:
    print(f"Error: {directory_to_delete} : {e.strerror}")

# run inference on the source (forward pass)
model.predict(args.file, save=True)
