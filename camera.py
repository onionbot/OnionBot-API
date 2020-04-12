import multiprocessing as mp

from time import sleep
from picamera import PiCamera


class Camera(object):
    def __init__(self):  # , *args, **kwargs

        print("Initialising camera...")

        camera = PiCamera()
        camera.rotation = 180
        camera.zoom = (0.05, 0.0, 0.75, 0.95)
        camera.resolution = (1024, 768)

        # camera.start_preview()
        self.camera = camera

    def _worker(self):
        print("Taking picture!")
        self.camera.capture(self.file_path, resize=(240, 240))

    def start(self, file_path):
        self.file_path = file_path
        self.p = mp.Process(target=self._worker)
        self.p.start()

    def join(self):
        self.p.join()
        return self.file_path
