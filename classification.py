from edgetpu.classification.engine import ClassificationEngine
from edgetpu.utils import dataset_utils
from PIL import Image
from threading import Thread, Event
from queue import Queue, Empty


import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Classify(object):
    """Save image to file"""

    def __init__(self):

        logger.info("Initialising classifier...")

        self.tests = {
            "pasta": {
                "labels": dataset_utils.read_label_file("models/pasta.txt"),
                "model": ClassificationEngine("models/pasta.tflite"),
                "threshold": 0.8,
            },
            "sauce": {
                "labels": dataset_utils.read_label_file("models/sauce.txt"),
                "model": ClassificationEngine("models/sauce.tflite"),
                "threshold": 0.8,
            },
            "pan_on_off": {
                "labels": dataset_utils.read_label_file("models/pan_on_off.txt"),
                "model": ClassificationEngine("models/pan_on_off.tflite"),
                "threshold": 0.5,
            },
        }

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

                for name, t in self.tests.items():

                    logger.debug("Starting test %s " % (name))

                    engine = t["model"]
                    labels = t["labels"]
                    threshold = t["threshold"]

                    result = engine.classify_with_image(
                        image, top_k=1, threshold=threshold
                    )
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
