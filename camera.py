import time
from time import sleep
from picamera import PiCamera

class Camera(object):
    
    def __init__(self):
        
        print ("Initialising camera...")

        camera = PiCamera()
        camera.rotation = 180
        camera.zoom = (0.05, 0.0, 0.75, 0.95)

        camera.resolution = (1024, 768)
        
        #camera.start_preview()
        self.camera=camera

    
    def capture(self, file_path):

        self.camera.capture(file_path, resize=(240, 240))
        
        return file_path
        
