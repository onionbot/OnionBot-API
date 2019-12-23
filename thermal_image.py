import os
import math
import time
import board
import busio
import pygame
from PIL import Image
import sys

import adafruit_mlx90640

INTERPOLATE = 10

MINTEMP = 20. #-40 #low range of the sensor (this will be black on the screen)
MAXTEMP = 50. #300 #high range of the sensor (this will be white on the screen)
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


class THERMAL_CAMERA(object):
    """Save image to file"""


    def __init__(self, i2c=None):

        self.latest_frame = None

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
        
        img_surface = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        pygame.transform.scale(img_surface.convert(), screen.get_size(), screen)
        pygame.display.update()
        print("Completed 2 frames in %0.2f s (%d FPS)" %
              (time.monotonic()-stamp, 1.0 / (time.monotonic()-stamp)))


    def capture_frame(self):

        frame = [0] * 768
        stamp = time.monotonic()
        try:
            self.mlx.getFrame(frame)
        except ValueError:
            print("ValueError: Retrying...")
            continue        # these happen, no biggie - retry

        print("Read 2 frames in %0.2f s" % (time.monotonic()-stamp))

        self.latest_frame = frame
        self.latest_stamp = stamp


    def get_latest_temperature(self):
        
        frame = self.latest_frame 

        if frame != None:
            h = 12
            w = 16        
            t = self.frame[h*32 + w]
            return t 


    def save_latest_jpg(self, path, visualise=False):

        frame = self.latest_frame 
        file_name = self.latest_stamp    
        
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
                sensorout.set_at((w, h), pixel)

        img = Image.new('RGB', (32, 24))
        img.putdata(pixels)
        img = img.resize((32*INTERPOLATE, 24*INTERPOLATE), Image.BICUBIC)
        img = img.transpose(method=Image.ROTATE_90)
        img = img.transpose(method=Image.FLIP_LEFT_RIGHT)

        file_path = path+"/"+file_name+".jpg"
        img.save(file_path)


        if visualise==True:
            self._visualise(img)



    def save_latest_csv(self, path):

        frame = self.latest_frame 
        file_name = self.latest_stamp

        data_string = []

        if frame != None:        
            for h in range(24):
                for w in range(32):
                    t = self.frame[h*32 + w]
                    data_string.append("%0.1f, " % t, end="")
            file_path = path+"/"+file_name+".csv"
            file = open(file_path)
            file.write(data_string)
            file.close()






    
