import threading
from time import sleep

from thermal_camera import ThermalCamera
from camera import Camera
from cloud import Cloud
from inference import Classify
from control import Control
from data import Data

import datetime
import json

import logging

FORMAT = "%(relativeCreated)6d %(levelname)-8s %(module)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

cloud = Cloud()
thermal = ThermalCamera()
camera = Camera()
control = Control()
data = Data()


class OnionBot(object):
    def __init__(self):

        # Launch multiprocessing threads
        camera.launch()
        thermal.launch()
        control.launch()
        self.exit_flag = False

        self.camera_sleep = 0

        self.measurement_id = 0
        self.active_label = None
        self.session_name = None

        self.latest_meta = json.dumps(
            data.generate_meta(
                session_name=self.session_name,
                time_stamp=0,
                measurement_id=self.measurement_id,
                active_label=self.active_label,
                hob_setpoint=control.get_setpoint(),
            )
        )

    def run(self):
        """Start logging"""

        def thread_function():
            """Threaded to run capture loop in background while allowing other processes to continue"""

            while self.exit_flag is False:

                # Get time stamp
                time_stamp = datetime.datetime.now()

                # Start cloud upload of previous images, handle first run exception
                try:
                    cloud.start(camera_filepath)
                    cloud.start(thermal_filepath)
                    cloud.start(thermal_history_filepath)
                except NameError:
                    logging.debug("First time exception")
                    previous_meta = self.latest_meta

                # If data saving active, save measurement ID

                self.measurement_id += 1

                measurement_id = self.measurement_id
                active_label = self.active_label
                session_name = self.session_name

                # Generate filepaths for logs
                (
                    camera_filepath,
                    thermal_filepath,
                    thermal_history_filepath,
                ) = data.generate_filepaths(
                    session_name, time_stamp, measurement_id, active_label
                )

                # Start sensor capture
                camera.start(camera_filepath)
                thermal.start(thermal_filepath, thermal_history_filepath)

                # Generate metadata
                metadata = data.generate_meta(
                    session_name=session_name,
                    time_stamp=time_stamp,
                    measurement_id=measurement_id,
                    active_label=active_label,
                    hob_setpoint=control.get_setpoint(),
                )

                # Wait for all processes to finish
                cloud.join()
                thermal.join()
                camera.join()

                # Shuffle metas
                self.latest_meta = previous_meta
                previous_meta = json.dumps(metadata)

                sleep(float(self.camera_sleep))

                logging.info(
                    "Logging %s | session_name %s | Label %s | Interval %0.3f s"
                    % (
                        measurement_id,
                        session_name,
                        active_label,
                        (datetime.datetime.now() - time_stamp).total_seconds(),
                    )
                )

            logging.info("Main thread exiting")

        # Start logging thread
        self.logging_thread = threading.Thread(target=thread_function)
        self.logging_thread.start()

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

        self.camera_sleep = value

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
        logging.info("Raising exit flag")
        self.exit_flag = True
        camera.quit()
        thermal.quit()
        cloud.quit()
        self.logging_thread.join(timeout=1)
