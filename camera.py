import multiprocessing as mp
from multiprocessing import JoinableQueue

from picamera import PiCamera

import logging
logger = logging.getLogger(__name__)


class Camera(object):
    def __init__(self):
        self.file_queue = JoinableQueue(1)

    def _worker(self):

        logger.info("Initialising camera")

        camera = PiCamera()
        camera.rotation = 180
        camera.zoom = (0.05, 0.0, 0.75, 0.95)
        camera.resolution = (1024, 768)

        while True:
            file_path = self.file_queue.get(block=True)

            logger.debug("Capturing image")
            camera.capture(file_path, resize=(240, 240))

            self.file_queue.task_done()

    def start(self, file_path):
        logger.debug("Calling start")
        self.file_queue.put(file_path, block=True)

    def join(self):
        logger.debug("Calling join")
        self.file_queue.join()

    def launch(self):
        logger.debug("Initialising worker")
        self.p = mp.Process(target=self._worker)
        self.p.start()

    def quit(self):
        logger.info("Quitting camera")
        self.file_queue.close()
        self.p.join(timeout=1)
