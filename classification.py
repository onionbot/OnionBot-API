from edgetpu.classification.engine import ClassificationEngine
from edgetpu.utils import dataset_utils
from PIL import Image
from threading import Thread, Event
from queue import Queue, Empty

from config import Classifiers
from json import dumps
from collections import deque
from statistics import mean

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

classifiers = Classifiers()


class Classify(object):
    """Save image to file"""

    def __init__(self):

        logger.info("Initialising classifier...")

        self.library = classifiers.get_classifiers()
        self.loaded = {}
        self.active = []

        self.quit_event = Event()
        self.file_queue = Queue()
        self.database = {}

    def _worker(self):

        logger.debug("Initialising classification worker")

        while True:
            try:  # Timeout raises queue.Empty

                image = self.file_queue.get(block=True, timeout=0.1)
                image = Image.open(image)

                library = self.library
                active = self.active
                database = self.database

                for name in library:

                    if name in active:
                        # Only classify active classifiers

                        logger.debug("Starting classifier %s " % (name))
                        engine = self.loaded[name]["model"]
                        labels = self.loaded[name]["labels"]
                        results = engine.classify_with_image(image, top_k=3)
                        logger.debug(results)

                        # Ensure classifer is in database
                        if name not in database:
                            database[name] = {}

                        # Iterate over classifier results
                        for result in results:
                            label = labels[result[0]]
                            confidence = result[1].item()
                            confidence = round(confidence, 2)

                            # Ensure label is in classifier database entry
                            if label not in database[name]:
                                database[name][label] = {}
                                database[name][label]["queue"] = [0] * 10

                            # Update nested database dictionary
                            result_data = database[name][label]
                            result_data["confidence"] = confidence

                            # Use deque to update average
                            queue = deque(result_data["queue"])
                            queue.append(confidence)
                            queue.popleft()
                            result_data["queue"] = list(queue)
                            average = round(sum(queue) / 10, 2)
                            result_data["average"] = average

                            for key, value in result_data:
                                print(type(result_data[key]))

                    elif name in database:
                        # Remove classifiers in database that are not active
                        del database[name]

                self.database = database

                logger.critical(database)

                self.file_queue.task_done()

            except Empty:
                if self.quit_event.is_set():
                    logger.debug("Quitting thread...")
                    break

    def load_classifiers(self, input_string):
        for name in input_string.split(","):

            # Check if classifier has already been loaded
            if name not in self.loaded:
                logger.debug("Loading classifier %s " % (name))

                # Read attributes from library and initialise
                try:
                    attr = self.library[name]
                    output = {}
                    output["labels"] = dataset_utils.read_label_file(attr["labels"])
                    output["model"] = ClassificationEngine(attr["model"])
                    self.loaded[name] = output
                except KeyError:
                    raise KeyError("Classifier name not found in database")
                except FileNotFoundError:
                    raise FileNotFoundError(
                        "Model or labels not found in models folder"
                    )

            else:
                logger.debug("Classifier already loaded %s " % (name))

    def set_classifiers(self, input_string):
        for name in input_string.split(","):

            # Check if classifier has already been loaded
            if name not in self.loaded:
                logger.debug("Classifier not loaded %s: loading " % (name))
                self.load_classifiers(name)
        self.active = input_string.split(",")

    def get_classifiers(self):
        return dumps(self.library)

    def start(self, file_path):
        logger.debug("Calling start")
        self.file_queue.put(file_path)

    def join(self):
        logger.debug("Calling join")
        self.file_queue.join()

    def launch(self):
        logger.debug("Initialising classification worker")
        self.thread = Thread(target=self._worker, daemon=True)
        self.thread.start()

    def quit(self):
        self.quit_event.set()
        logger.debug("Waiting for classification thread to finish")
        self.thread.join()
