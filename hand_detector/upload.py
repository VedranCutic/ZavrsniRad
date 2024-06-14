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
    # Set device to CPU explicitly
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load model and move it to the correct device
    model = YOLO("lewiswatson/yolov8x-tuned-hand-gestures").to(device)
    print(model.model.names)

    # model.model.names[15] = "back-fist"
    # model.model.names[16] = "front-fist"
    # model.model.names[18] = "two"
    # model.model.names[19] = "open-palm"
    # model.model.names[20] = "thumbs-up"
    # model.model.names[8] = "one"

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
