import argparse
import curses
import json
import time

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--filename",
    help="input filename",
    type=str,
    required=True
)
args = parser.parse_args()

with open(args.filename, "r") as f:
    data = json.load(f)

sleep_time = 1 / data["fps"]
frames = data["frames"]

w, h = len(frames[0][0]), len(frames[0])

stdscr = curses.initscr()
stdscr.resize(h, w * 2)
for frame in frames:
    try:
        for pos, line in enumerate(frame):
            stdscr.addstr(pos, 0, " ".join(line))
    except Exception:
        pass

    stdscr.refresh()

    time.sleep(sleep_time)
curses.endwin()
