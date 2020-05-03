from threading import Thread, Event
from time import sleep, strftime

from thermal_camera import ThermalCamera
from camera import Camera
from cloud import Cloud
from inference import Classify
from control import Control
from data import Data
from config import Config

import datetime
import json

import logging

# Fix logging faliure issue
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

FORMAT = "%(relativeCreated)6d %(levelname)-8s %(name)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


cloud = Cloud()
thermal = ThermalCamera()
camera = Camera()
control = Control()
data = Data()
config = Config()


class OnionBot(object):
    def __init__(self):

        self.quit_event = Event()

        # Launch multiprocessing threads
        logger.info("Launching worker threads")
        camera.launch()
        thermal.launch()
        control.launch()

        self.latest_meta = "None"
        self.measurement_id = 0
        self.session_name = None
        self.active_label = None

    def run(self):
        """Start logging"""

        def _worker():
            """Threaded to run capture loop in background while allowing other processes to continue"""

            data_published = False

            while True:

                # Get time stamp
                timer = datetime.datetime.now()

                time_stamp = strftime("%Y-%m-%d_%H-%M-%S-%f")

                self.measurement_id += 1
                measurement_id = self.measurement_id
                active_label = self.active_label
                session_name = self.session_name

                # Generate filepaths for logs
                filepaths = data.generate_filepaths(
                    session_name, time_stamp, measurement_id, active_label
                )
                camera_filepath = filepaths["camera"]
                thermal_filepath = filepaths["thermal"]
                thermal_history_filepath = filepaths["thermal_history"]

                # Start sensor capture
                camera.start(camera_filepath)
                thermal.start(thermal_filepath, thermal_history_filepath)

                # While taking a picture, see if there is previous data to process
                if data_published:

                    cloud.start(previous_camera_filepath)
                    cloud.start(previous_thermal_filepath)
                    cloud.start(previous_thermal_history_filepath)

                    # inference.start(previous_meta)

                    # Wait for all processes to finish
                    cloud.join()
                    # inference.join()

                    # Generate metadata
                    metadata = data.generate_meta(
                        filepaths=filepaths,
                        session_name=session_name,
                        time_stamp=time_stamp,
                        measurement_id=measurement_id,
                        active_label=active_label,
                        hob_setpoint=control.get_actual(),
                    )

                    self.latest_meta = metadata

                previous_camera_filepath = camera_filepath
                previous_thermal_filepath = thermal_filepath
                previous_thermal_history_filepath = thermal_history_filepath

                data_published = True
                logger.info(
                    "Logged %s | session_name %s | Label %s | Interval %0.3f s"
                    % (
                        measurement_id,
                        session_name,
                        active_label,
                        (datetime.datetime.now() - timer).total_seconds(),
                    )
                )

                # temp, thermal history = thermal.join()
                thermal.join()
                camera.join()
                # Servo get values, history

                # Add delay until next reading
                sleep(float(config.get_config("camera_sleep")))

                # Check quit flag
                if self.quit_event.is_set():
                    logger.debug("Quitting main thread...")
                    break

        # Start thread
        self.thread = Thread(target=_worker)
        self.thread.start()

    def start(self, session_name):

        self.session_name = session_name

        return "success"

    def stop(self):
        """Stop logging"""

        self.session_name = None

        return "success"

    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return self.latest_meta

    def get_thermal_history(self):
        """Returns last 300 temperature readings"""

        return self.thermal_history

    def get_chosen_labels(self):
        """Returns options for labels selected from `all_labels` in new session process"""

        # (Placeholder) TODO: Update to return list of labels that adapts to selected dropdown
        return '[{"ID":"0","label":"discard"},{"ID":"1","label":"water_boiling"},{"ID":"2","label":"water_not_boiling"}]'

    def set_chosen_labels(self, string):
        """Returns options for labels selected from `all_labels` in new session process"""

        self.chosen_labels = string
        return "success"

    def set_active_label(self, string):
        """Command to change current active label -  for building training datasets"""

        self.active_label = string
        return "success"

    def set_active_model(self, string):
        """Command to change current active model for predictions"""

        if string == "tflite_water_boiling_1":
            self.camera_classifier = Classify(
                labels="models/tflite-boiling_water_1_20200111094256-2020-01-11T11_51_24.886Z_dict.txt",
                model="models/tflite-boiling_water_1_20200111094256-2020-01-11T11_51_24.886Z_model.tflite",
            )
            self.thermal_classifier = Classify(
                labels="models/tflite-boiling_1_thermal_20200111031542-2020-01-11T18_45_13.068Z_dict.txt",
                model="models/tflite-boiling_1_thermal_20200111031542-2020-01-11T18_45_13.068Z_model.tflite",
            )
            self.active_model = string

        return "success"

    def set_hob_setpoint(self, value):
        """Command to change current temperature setpoint"""

        control.update_setpoint(value)
        self.hob_setpoint = value

        return "success"

    def set_hob_off(self):
        """Command to turn hob off"""

        control.hob_off()
        self.hob_setpoint = "OFF"

        return "success"

    def set_camera_sleep(self, value):
        """Command to change camera targe refresh rate"""

        config.set_config("camera_sleep", value)

        return "success"

    def get_all_labels(self):
        """Returns available image labels for training"""

        # data = '[{"ID":"0","label":"discard,water_boiling,water_not_boiling"},{"ID":"1","label":"discard,onions_cooked,onions_not_cooked"}]'
        labels = json.dumps(data.generate_labels())

        return labels

    def get_all_models(self):
        """Returns available models for prediction"""

        data = '[{"ID":"0","label":"tflite_water_boiling_1"}]'

        return data

    def quit(self):
        logger.info("Raising exit flag")
        self.quit_event.set()
        camera.quit()
        thermal.quit()
        cloud.quit()
        control.quit()
        self.thread.join(timeout=1)
