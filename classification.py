from edgetpu.classification.engine import ClassificationEngine
from edgetpu.utils import dataset_utils
from PIL import Image
from threading import Thread, Event
from queue import Queue, Empty

from config import Classifiers
from json import dumps

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

classifiers = Classifiers()


class Classify(object):
    """Save image to file"""

    def __init__(self):

        logger.info("Initialising classifier...")

        self.all = classifiers.get_classifiers()
        self.loaded = {}
        self.active = []

        self.quit_event = Event()
        self.file_queue = Queue()
        self.data = None

    def _worker(self):

        logger.debug("Initialising classification worker")

        while True:
            try:  # Timeout raises queue.Empty

                image = self.file_queue.get(block=True, timeout=0.1)
                image = Image.open(image)

                output = {}

                for name in self.active:

                    c = self.loaded[name]

                    logger.debug("Starting classifier %s " % (name))

                    engine = c["model"]
                    labels = c["labels"]

                    result = engine.classify_with_image(image, top_k=1)
                    logger.debug(result)

                    try:
                        result = result[0]
                        output[name] = {
                            "label": labels[result[0]],
                            "confidence": str(result[1]),
                        }
                    except TypeError:
                        logger.debug("TypeError")
                    except IndexError:
                        logger.debug("IndexError")
                logger.debug(output)
                self.data = output
                self.file_queue.task_done()

            except Empty:
                if self.quit_event.is_set():
                    logger.debug("Quitting thread...")
                    break

    def load_classifiers(self, input_string):
        for name in input_string.split(","):
            if name not in self.loaded:
                logger.debug("Loading classifier %s " % (name))
                try:
                    attr = self.all[name]
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
            if name not in self.loaded:
                logger.debug("Classifier not loaded %s " % (name))
                self.load_classifiers(name)
        self.active = input_string.split(",")

    def get_classifiers(self):
        return dumps(self.all)

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
