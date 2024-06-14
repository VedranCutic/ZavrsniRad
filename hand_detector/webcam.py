from ultralyticsplus import YOLO
import torch
import cv2
import numpy as np
import supervision as sv
import argparse


def arguments_parser():
    parser = argparse.ArgumentParser(description="arguments parser")
    parser.add_argument("--resolution", default=[1280, 640], nargs=2, type=int)
    parser.add_argument("--model")
    args = parser.parse_args()
    return args


########
# MAIN #
########


args = arguments_parser()
width, height = args.resolution


if args.model == "pretrained":
    # Set device to CPU explicitly
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load model and move it to the correct device
    model = YOLO("lewiswatson/yolov8x-tuned-hand-gestures").to(device)

    # model.model.names[15] = "back-fist"
    # model.model.names[16] = "front-fist"
    # model.model.names[18] = "two"
    # model.model.names[19] = "open-palm"
    # model.model.names[20] = "thumbs-up"
    # model.model.names[8] = "one"

elif args.model == "trained":
    print("running on trained data")
    model = YOLO("best2.pt")
    model.model.names[0] = "palm"
    model.model.names[1] = "palm"


box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)


# 0 is for webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

while True:
    ret, frame = cap.read()

    result = model(frame)[0]
    detections = sv.Detections.from_yolov8(result)

    labels = [
        f"{model.model.names[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, _ in detections
    ]

    frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)

    cv2.imshow("Hand Detection", frame)
    # 27 is ESC in ascii
    if cv2.waitKey(30) == 27:  # & 0xFF == ord("q"):
        break
