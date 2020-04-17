import multiprocessing as mp
from multiprocessing import JoinableQueue

import math
from statistics import mode, StatisticsError
import time
import board
import busio
import json
from PIL import Image
from collections import deque

import adafruit_mlx90640
import logging

INTERPOLATE = 10

MINTEMP = 20.0  # -40 #low range of the sensor (this will be black on the screen)
MAXTEMP = 200.0  # previous 50 #max 300 #high range of the sensor (this will be white on the screen)
SCALE = 25


# the list of colors we can choose from
heatmap = (
    (0.0, (0, 0, 0)),
    (0.20, (0, 0, 0.5)),
    (0.40, (0, 0.5, 0)),
    (0.60, (0.5, 0, 0)),
    (0.80, (0.75, 0.75, 0)),
    (0.90, (1.0, 0.75, 0)),
    (1.00, (1.0, 1.0, 1.0)),
)

# how many color values we can have
COLORDEPTH = 1000

colormap = [0] * COLORDEPTH


class ThermalCamera(object):
    """Save image to file"""

    def __init__(self, i2c=None, visualise_on=False):

        logging.info("Initialising thermal camera...")

        if i2c is None:
            i2c = busio.I2C(board.SCL, board.SDA)

        mlx = adafruit_mlx90640.MLX90640(i2c)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ

        self.mlx = mlx

        self.file_queue = JoinableQueue(1)

    def _constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))

    def _map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def _gaussian(self, x, a, b, c, d=0):
        return a * math.exp(-((x - b) ** 2) / (2 * c ** 2)) + d

    def _gradient(self, x, width, cmap, spread=1):
        width = float(width)
        r = sum(
            [
                self._gaussian(x, p[1][0], p[0] * width, width / (spread * len(cmap)))
                for p in cmap
            ]
        )
        g = sum(
            [
                self._gaussian(x, p[1][1], p[0] * width, width / (spread * len(cmap)))
                for p in cmap
            ]
        )
        b = sum(
            [
                self._gaussian(x, p[1][2], p[0] * width, width / (spread * len(cmap)))
                for p in cmap
            ]
        )
        r = int(self._constrain(r * 255, 0, 255))
        g = int(self._constrain(g * 255, 0, 255))
        b = int(self._constrain(b * 255, 0, 255))
        return r, g, b

    def _worker(self):
        def _value(frame, history_file_path, thermal_history):

            logging.debug("Proccessing numerical data")

            h = 12
            w = 16
            t = frame[h * 32 + w]
            t = "{:.1f}".format(t)

            thermal_history.append(t)
            thermal_history.popleft()

            data = {
                "type": "thermal_history",
                "attributes": {
                    "data": list(thermal_history),
                },
            }

            with open(history_file_path, "w") as write_file:
                    json.dump(data, write_file)

            return thermal_history

        def _image(frame, file_path):

            logging.debug("Proccessing image data")

            for i in range(COLORDEPTH):
                colormap[i] = self._gradient(i, COLORDEPTH, heatmap)

            pixels = [0] * 768
            for i, pixel in enumerate(frame):
                coloridx = self._map_value(pixel, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1)
                coloridx = int(self._constrain(coloridx, 0, COLORDEPTH - 1))
                pixels[i] = colormap[coloridx]

            img = Image.new("RGB", (32, 24))
            img.putdata(pixels)
            img = img.resize((24 * INTERPOLATE, 24 * INTERPOLATE), Image.BICUBIC)

            img = img.transpose(method=Image.ROTATE_90)
            img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
            img.save(file_path)

        thermal_history = deque([0] * 120)

        while True:
            paths = self.file_queue.get(block=True)

            [file_path, history_file_path] = paths

            logging.debug("Capturing frame")
            frame = [0] * 768
            stamp = time.monotonic()
            while True:
                try:
                    print("Click")
                    self.mlx.getFrame(frame)
                    try:
                        if mode(frame) == 0: # Handle chessboard error
                            logging.info("Frame capture ZERO error, retrying")
                            raise ValueError
                    except StatisticsError: # Handle more than one modal value
                        break # Modes > 1 means that chessboard error must not have happened
                    break
                except ValueError: # Handle ValueError in module
                    logging.info("Frame capture error, retrying")

            logging.debug("Read 2 frames in %0.3f s" % (time.monotonic() - stamp))

            thermal_history = _value(frame, history_file_path, thermal_history)

            _image(frame, file_path)

            self.file_queue.task_done()

    def start(self, file_path, history_file_path):
        logging.debug("Calling start")
        self.file_queue.put([file_path, history_file_path], block=True)

    def join(self):
        logging.debug("Calling join")
        self.file_queue.join()

    def launch(self):
        logging.debug("Initialising worker")
        self.p = mp.Process(target=self._worker)
        self.p.start()

    def quit(self):
        logging.info("Quitting thermal camera")
        self.file_queue.close()
        self.p.join(timeout=1)

