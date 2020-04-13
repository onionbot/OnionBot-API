import os
from google.cloud import storage
import logging
import multiprocessing as mp

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

bucket_name = "onionbucket"


class Cloud(object):
    """Save image to file"""

    def __init__(self):
        self.processes = []

    def _worker(self, path):

        logging.info("Initialising upload worker")

        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        blob = bucket.blob(path)
        blob.upload_from_filename(path)
        blob.make_public()
        # print("Uploaded to cloud:", path)
        # print("Blob is publicly accessible at ", blob.public_url)

    def start(self, path):

        logging.debug("Calling start")

        process = mp.Process(target=self._worker, args=(path,))
        process.start()

        self.processes.append(process)

    def join(self):

        [p.join() for p in self.processes]
        self.processes = []

    def get_path(self, session_name, sensor, file_type, time, measurement_id, label):

        # Make local path
        time_data = time.strftime("%Y-%m-%d_%H-%M-%S-%f")
        path = f"logs/{session_name}/{sensor}/{label}"
        filename = f"{session_name}_{str(measurement_id).zfill(5)}_{time_data}_{sensor}_{label}.{file_type}"
        os.makedirs(path, exist_ok=True)

        return f"{path}/{filename}"

    def get_public_path(self, local_path):

        # Public URL
        cloud_location = "https://storage.googleapis.com/" + bucket_name

        return f"{cloud_location}/{local_path}"
