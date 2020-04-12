import multiprocessing as mp
from multiprocessing import JoinableQueue

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

    def capture(self, file_path):
        self.intray.put(file_path)
        

    def thread(self):
        while True:
            file_path = self.intray.get(block=True)
            self.camera.capture(file_path, resize=(240, 240))

    def run(self):

        self.intray = JoinableQueue(2)

        p = mp.Process(target=self.thread)
        p.start()


if __name__ == "__main__":
    a = A()
    a.run()
