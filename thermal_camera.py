import math
import time
import board
import busio
from PIL import Image
from collections import deque
import json

import adafruit_mlx90640

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

        print("Initialising thermal camera...")

        self._latest_frame = None
        self.visualise_on = visualise_on

        if i2c is None:
            i2c = busio.I2C(board.SCL, board.SDA)

        mlx = adafruit_mlx90640.MLX90640(i2c)
        print(
            "  * MLX addr detected on I2C, Serial #",
            [hex(i) for i in mlx.serial_number],
        )
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ
        print("  * Refresh rate: ", pow(2, (mlx.refresh_rate - 1)), "Hz")

        self.mlx = mlx

        self.temperature_window = deque([0] * 10)

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

    def capture_frame(self):

        frame = [0] * 768
        stamp = time.monotonic()
        try:
            self.mlx.getFrame(frame)
        except ValueError:
            print("ValueError: Retrying...")

        print("Read 2 frames in %0.3f s" % (time.monotonic() - stamp))

        self._latest_frame = frame
        self._latest_stamp = stamp

    def get_latest_temperature(self):

        frame = self._latest_frame

        if frame == None:
            raise ValueError("Run capture function first")
        elif frame != None:
            h = 12
            w = 16
            t = self._latest_frame[h * 32 + w]
            temperature = "{:.1f}".format(t)

            self.temperature_window.append(t)
            self.temperature_window.popleft()

            return temperature

    def get_temperature_window(self):

        return json.dumps(list(self.temperature_window))

    def save_latest_jpg(self, file_path):

        frame = self._latest_frame
        file_name = str(self._latest_stamp)

        if frame == None:
            raise ValueError("Run capture function first")

        for i in range(COLORDEPTH):
            colormap[i] = self._gradient(i, COLORDEPTH, heatmap)

        pixels = [0] * 768
        for i, pixel in enumerate(frame):
            coloridx = self._map_value(pixel, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1)
            coloridx = int(self._constrain(coloridx, 0, COLORDEPTH - 1))
            pixels[i] = colormap[coloridx]

        for h in range(24):
            for w in range(32):
                pixel = pixels[h * 32 + w]
                if self.visualise_on == True:
                    self.sensorout.set_at((w, h), pixel)

        img = Image.new("RGB", (32, 24))
        img.putdata(pixels)
        img = img.resize((24 * INTERPOLATE, 24 * INTERPOLATE), Image.BICUBIC)

        img = img.transpose(method=Image.ROTATE_90)
        img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        img.save(file_path)

        return file_path
