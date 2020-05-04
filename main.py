from threading import Thread, Event
from time import sleep

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

        self.latest_meta = " "
        self.measurement_id = 0
        self.session_name = None
        self.active_label = None

    def run(self):
        """Start logging"""

        def _worker():
            """Threaded to run capture loop in background while allowing other processes to continue"""

            filepaths = None
            meta = None

            while True:

                # Get time stamp
                timer = datetime.datetime.now()
                time_stamp = timer.strftime("%Y-%m-%d_%H-%M-%S-%f")

                # Get update on key information
                self.measurement_id += 1
                measurement_id = self.measurement_id
                active_label = self.active_label
                session_name = self.session_name

                # Generate filepaths for logs
                queued_filepaths = data.generate_filepaths(
                    session_name, time_stamp, measurement_id, active_label
                )

                # Generate metadata for frontend
                queued_meta = data.generate_meta(
                    session_name=session_name,
                    time_stamp=time_stamp,
                    measurement_id=measurement_id,
                    active_label=active_label,
                    filepaths=queued_filepaths,
                    thermal_data=thermal.data,
                    control_data=control.data,
                )

                # Start sensor capture
                camera.start(queued_filepaths["camera"])
                thermal.start(queued_filepaths["thermal"])

                # While taking a picture, process previous data in meantime
                if filepaths:

                    cloud.start(filepaths["camera"])
                    cloud.start(filepaths["thermal"])

                    # inference.start(previous_meta)

                    # Wait for all meantime processes to finish
                    if not cloud.join():
                        meta["attributes"]["camera_filepath"] = "placeholder.png"
                        meta["attributes"]["thermal_filepath"] = "placeholder.png"
                    # inference.join()

                    # Push meta information to file level for API access
                    self.latest_meta = json.dumps(meta)

                # Wait for queued image captures to finish, refresh control data
                thermal.join()
                camera.join()
                control.refresh()

                # Log to console
                logger.info(
                    "Logged %s | session_name %s | Label %s | Interval %0.2f | Temperature %s | Temperature Variance %s "
                    % (
                        measurement_id,
                        session_name,
                        active_label,
                        (datetime.datetime.now() - timer).total_seconds(),
                        thermal.data["temperature"],
                        thermal.data["variance"],
                    )
                )

                # Move queue forward one place
                filepaths = queued_filepaths
                meta = queued_meta

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

    def set_fixed_setpoint(self, value):
        """Command to change fixed setpoint"""

        control.update_fixed_setpoint(value)

        return "success"

    def set_temperature_target(self, value):
        """Command to change temperature target"""

        control.update_temperature_target(value)

        return "success"

    def set_hob_off(self):
        """Command to turn hob off"""

        control.hob_off()

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
        self.thread.join()
        logger.info("Main module quit")
        camera.quit()
        logger.info("Camera module quit")
        thermal.quit()
        logger.info("Thermal module quit")
        cloud.quit()
        logger.info("Cloud module quit")
        control.quit()
        logger.info("Control module quit")
        logger.info("Success")
