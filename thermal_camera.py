import os
import math
import time
import board
import busio
from PIL import Image
import sys
from collections import deque
import json

import adafruit_mlx90640

INTERPOLATE = 10

MINTEMP = 20. #-40 #low range of the sensor (this will be black on the screen)
MAXTEMP = 200. #previous 50 #max 300 #high range of the sensor (this will be white on the screen)
SCALE = 25


#the list of colors we can choose from
heatmap = (
    (0.0, (0, 0, 0)),
    (0.20, (0, 0, .5)),
    (0.40, (0, .5, 0)),
    (0.60, (.5, 0, 0)),
    (0.80, (.75, .75, 0)),
    (0.90, (1.0, .75, 0)),
    (1.00, (1.0, 1.0, 1.0)),
)

#how many color values we can have
COLORDEPTH = 1000

colormap = [0] * COLORDEPTH


class ThermalCamera(object):
    """Save image to file"""


    def __init__(self, i2c=None, visualise_on=False):

        self._latest_frame = None
        self.visualise_on = visualise_on

        if i2c is None:
            # MUST et I2C freq to 1MHz in /boot/config.txt
            i2c = busio.I2C(board.SCL, board.SDA)
        
        #initialize the sensor
        mlx = adafruit_mlx90640.MLX90640(i2c)
        print("MLX addr detected on I2C, Serial #", [hex(i) for i in mlx.serial_number])
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ
        print(mlx.refresh_rate)
        print("Refresh rate: ", pow(2, (mlx.refresh_rate-1)), "Hz")

        self.mlx = mlx

        self.temperature_window = deque([0] * 10)
        
        if visualise_on == True:
            
            import pygame
            
            # set up display
            os.environ['SDL_FBDEV'] = "/dev/fb0"
            os.environ['SDL_VIDEODRIVER'] = "fbcon"
            pygame.init()
            screen = pygame.display.set_mode((24*SCALE,32*SCALE))
            print(pygame.display.Info())

            pygame.mouse.set_visible(False)
            screen.fill((255, 0, 0))
            pygame.display.update()
            screen.fill((0, 0, 0))
            pygame.display.update()
            sensorout = pygame.Surface((32, 24))
            
            self.screen = screen
            self.sensorout = sensorout


    def _constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))


    def _map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


    def _gaussian(self, x, a, b, c, d=0):
        return a * math.exp(-(x - b)**2 / (2 * c**2)) + d


    def _gradient(self, x, width, cmap, spread=1):
        width = float(width)
        r = sum([self._gaussian(x, p[1][0], p[0] * width, width/(spread*len(cmap))) for p in cmap])
        g = sum([self._gaussian(x, p[1][1], p[0] * width, width/(spread*len(cmap))) for p in cmap])
        b = sum([self._gaussian(x, p[1][2], p[0] * width, width/(spread*len(cmap))) for p in cmap])
        r = int(self._constrain(r*255, 0, 255))
        g = int(self._constrain(g*255, 0, 255))
        b = int(self._constrain(b*255, 0, 255))
        return r, g, b


    def _visualise(self, img):
        
        stamp = self._latest_stamp
        screen = self.screen
        
        img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        pygame.transform.scale(img_surface.convert(),screen.get_size(), screen)
        pygame.display.update()
        print("Completed 2 frames in %0.2f s (%d FPS)" %
              (time.monotonic()-stamp, 1.0 / (time.monotonic()-stamp)))
        
        time.sleep(10)


    def capture_frame(self):

        frame = [0] * 768
        stamp = time.monotonic()
        try:
            self.mlx.getFrame(frame)
        except ValueError:
            print("ValueError: Retrying...")

        #print("Read 2 frames in %0.2f s" % (time.monotonic()-stamp))

        self._latest_frame = frame
        self._latest_stamp = stamp


    def get_latest_temperature(self):
        
        frame = self._latest_frame
        
        if frame == None:
            raise ValueError("Run capture function first")
        elif frame != None:
            h = 12
            w = 16        
            t = self._latest_frame[h*32 + w]
            temperature = "{:.1f}".format(t)

            self.temperature_window.append(temperature)
            self.temperature_window.popleft()

            return temperature


    def get_temperature_window(self):

        return json.dumps(self.temperature_window)


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
            coloridx = int(self._constrain(coloridx, 0, COLORDEPTH-1))
            pixels[i] = colormap[coloridx]

        for h in range(24):
            for w in range(32):
                pixel = pixels[h*32 + w]
                if self.visualise_on==True:
                    self.sensorout.set_at((w, h), pixel)

        img = Image.new('RGB', (32, 24))
        img.putdata(pixels)
        img = img.resize((24*INTERPOLATE, 24*INTERPOLATE), Image.BICUBIC)
        
        img = img.transpose(method=Image.ROTATE_90)
        img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        img.save(file_path)

        if self.visualise_on==True:
            self._visualise(img)
            
        return file_path


    def save_latest_csv(self, file_path):

        frame = self._latest_frame 
        file_name = str(self._latest_stamp)

        if frame == None:
            raise ValueError("Run capture function first")

        file = open(file_path, "w")
        for h in range(24):
            data_string = ""
            for w in range(32):
                t = self._latest_frame[h*32 + w]
                data_string = data_string + "{:.1f}".format(t) + ","
            file.write(data_string.strip(',') + "\n")
            
        file.close()

        return file_path




    
