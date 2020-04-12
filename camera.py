import logging

logging.basicConfig(level=logging.DEBUG)

import multiprocessing as mp
from multiprocessing import JoinableQueue

from time import sleep
from picamera import PiCamera


class Camera(object):
    def __init__(self): 

        self.file_queue = JoinableQueue(1)
        self._launch()

    def _worker(self):

        logging.info("Initialising camera")

        camera = PiCamera()
        camera.rotation = 180
        camera.zoom = (0.05, 0.0, 0.75, 0.95)
        camera.resolution = (1024, 768)

        while True:
            file_name = self.file_queue.get(block=True)

            logging.debug("Capturing image")
            camera.capture(file_name, resize=(240, 240))

            self.file_queue.task_done()

    def start(self, file_name):
        logging.debug("Calling start")
        self.file_queue.put(file_name, block=True)

    def join(self):
        logging.debug("Calling join")
        self.file_queue.join()

    def _launch(self):
        logging.debug("Initialising worker")
        p = mp.Process(target=self._worker)
        p.start()
