import os
from google.cloud import storage
from threading import Thread

import logging
logger = logging.getLogger(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

bucket_name = "onionbucket"


class Cloud(object):
    """Save image to file"""

    def __init__(self):
        self.threads = []

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

        thread = Thread(target=self._worker, args=(path,))
        thread.start()

        self.threads.append(thread)

    def join(self):
        [t.join() for t in self.threads]
        self.threads = []

    def quit(self):
        logger.debug("Quitting cloud")
        [p.join(timeout=1) for p in self.threades]

    def get_public_path(self, local_path):

        if local_path:
            # Public URL
            cloud_location = "https://storage.googleapis.com/" + bucket_name

            return f"{cloud_location}/{local_path}"
        else:
            return None
