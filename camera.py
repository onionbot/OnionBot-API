import logging

logging.basicConfig(level=logging.DEBUG)

import multiprocessing as mp
from multiprocessing import JoinableQueue

from time import sleep
from picamera import PiCamera


class Camera(object):
    def __init__(self):  # , *args, **kwargs

        logging.info("Initialising camera...")

        camera = PiCamera()
        camera.rotation = 180
        camera.zoom = (0.05, 0.0, 0.75, 0.95)
        camera.resolution = (1024, 768)

        # camera.start_preview()
        self.camera = camera

    def _worker(self, file_path):
        logging.debug("Capture process started")
        logging.debug(file_path)
        self.camera.capture(file_path, resize=(240, 240))
        logging.debug("Captured, putting file path in queue")
        self.file_queue.put(file_path)

    def start(self, file_path):
        logging.debug("Start called")

        self.file_queue = JoinableQueue()

        p = mp.Process(target=self._worker, args=(file_path, ))
        p.start()
        p.join()

    def join(self):
        logging.debug("Calling file join...")
        file_path = self.file_queue.join()
        logging.debug("File joined")
        file_queue.close()
        logging.debug("Queue closed")
        return file_path
