import os
from google.cloud import storage
import multiprocessing as mp

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

bucket_name = "onionbucket"


class Cloud(object):
    """Save image to file"""

    def __init__(self):
        self.processes = []

    def _worker(self, path):

        logger.debug("Initialising upload worker")

        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        blob = bucket.blob(path)
        blob.upload_from_filename(path)
        blob.make_public()
        logger.debug("Uploaded to cloud: %s" % (path))
        logger.debug("Blob is publicly accessible at %s" % (blob.public_url))

    def start(self, path):

        logger.debug("Calling start")

        process = mp.Process(target=self._worker, args=(path,))
        process.start()

        self.processes.append(process)

    def join(self):
        [p.join() for p in self.processes]
        self.processes = []

    def quit(self):
        logger.debug("Quitting cloud")
        [p.join(timeout=1) for p in self.processes]

    def get_public_path(self, local_path):

        if local_path:
            # Public URL
            cloud_location = "https://storage.googleapis.com/" + bucket_name

            return f"{cloud_location}/{local_path}"
        else:
            return None
