import argparse
import json

import cv2 as cv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="input filename", type=str, required=True)
parser.add_argument(
    "-p",
    "--pixels",
    help="custom ASCII brightness pixels",
    type=str,
    default=" .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
)
parser.add_argument("-o", "--output", help="output filename", type=str, required=True)
parser.add_argument(
    "-s", "--size", help="Output animation size (e.g. 80x60)", type=str, required=True
)
args = parser.parse_args()

filename = args.filename
size = tuple(map(int, args.size.split("x")))
output = args.output
pixels = args.pixels

cap = cv.VideoCapture(filename)
fps = int(cap.get(cv.CAP_PROP_FPS))
frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

frames = []
for _ in range(frame_count):
    _, raw_frame = cap.read()
    frame = cv.cvtColor(raw_frame, cv.COLOR_BGR2GRAY)
    frame = cv.resize(frame, size, interpolation=cv.INTER_AREA)

    res = []

    percents = frame / 255
    indexes = (percents * (len(pixels) - 1)).astype(np.int64)

    h, w = frame.shape

    for i in range(h):
        row = ""
        for j in range(w):
            row += pixels[indexes[i][j]]
        res.append(row)

    frames.append(res)
cap.release()

with open(output, "w") as f:
    json.dump({"fps": fps, "frames": frames}, f)
