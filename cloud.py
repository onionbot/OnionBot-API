from os import environ, path
from google.cloud import storage
from threading import Thread, Event
from queue import Queue, Empty

import logging

logger = logging.getLogger(__name__)

environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

BUCKET = "onionbucket" 
PATH = path.dirname(__file__)


class Cloud(object):
    """Save image to file"""

    def __init__(self):

        logger.info("Initialising cloud upload...")

        self.quit_event = Event()
        self.thermal_file_queue = Queue()
        self.camera_file_queue = Queue()
        self.bucket = BUCKET

    def _camera_worker(self):

        logger.debug("Initialising upload worker for camera")

        client = storage.Client()
        bucket = client.get_bucket(BUCKET)

        while True:
            try:  # Timeout raises queue.Empty
                local_path = self.camera_file_queue.get(block=True, timeout=0.1)
                local_path = local_path.replace(PATH + "/", "")
                cloud_path = local_path.replace(BUCKET + "/", "")

                blob = bucket.blob(cloud_path)
                blob.upload_from_filename(local_path)
                blob.make_public()
                logger.info("Uploaded camera file to cloud: %s" % (local_path))
                logger.info("Blob is publicly accessible at %s" % (blob.public_url))

                self.camera_file_queue.task_done()

            except Empty:
                if self.quit_event.is_set():
                    logger.debug("Quitting camera camera thread...")
                    break

    def start_camera(self, file_path):
        logger.debug("Calling start for camera")
        self.camera_file_queue.put(file_path)

    def join_camera(self):
        logger.debug("Calling join for camera")
        self.camera_file_queue.join()

    def launch_camera(self):
        logger.debug("Initialising worker for camera")
        self.camera_thread = Thread(target=self._camera_worker, daemon=True)
        self.camera_thread.start()

    def _thermal_worker(self):

        logger.debug("Initialising upload worker for thermal")

        client = storage.Client()
        bucket = client.get_bucket(BUCKET)

        while True:
            try:  # Timeout raises queue.Empty
                local_path = self.thermal_file_queue.get(block=True, timeout=0.1)
                local_path = local_path.replace(PATH + "/", "")
                cloud_path = local_path.replace(BUCKET + "/", "")

                blob = bucket.blob(cloud_path)
                blob.upload_from_filename(local_path)
                blob.make_public()
                logger.info("Uploaded camera file to cloud: %s" % (local_path))
                logger.info("Blob is publicly accessible at %s" % (blob.public_url))

                self.thermal_file_queue.task_done()

            except Empty:
                if self.quit_event.is_set():
                    logger.debug("Quitting thermal camera thread...")
                    break

    def start_thermal(self, file_path):
        logger.debug("Calling start for thermal")
        self.thermal_file_queue.put(file_path)

    def join_thermal(self):
        logger.debug("Calling join for thermal")
        self.thermal_file_queue.join()

    def launch_thermal(self):
        logger.debug("Initialising worker for thermal")
        self.thermal_thread = Thread(target=self._thermal_worker, daemon=True)
        self.thermal_thread.start()

    def get_public_path(self, local_path):
        if local_path:
            local_path = local_path.replace(PATH + "/", "")
            cloud_location = "https://storage.googleapis.com/" + BUCKET

            return f"{cloud_location}/{local_path}"
        else:
            return None

    def quit(self):
        self.quit_event.set()
        logger.debug("Waiting for camera cloud thread to finish uploading")
        self.camera_thread.join()
        logger.debug("Waiting for thermal cloud thread to finish uploading")
        self.thermal_thread.join()
