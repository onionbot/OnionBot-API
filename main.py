import multiprocessing as mp
from time import sleep

from thermal_camera import ThermalCamera
from camera import Camera
from cloud import Cloud
from inference import Classify
from actuation import Servo
from data import Data

import datetime
import json

import logging

FORMAT = "%(relativeCreated)6d %(levelname)-8s %(module)s %(process)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

cloud = Cloud()
thermal = ThermalCamera(visualise_on=False)
camera = Camera()
servo = Servo()
data = Data()


class OnionBot(object):
    def __init__(self):

        # Launch multiprocessing threads and store!!!
        camera.launch()
        thermal.launch()

        self.camera_sleep = "0"
        self.hob_setpoint = "0"

        self.measurement_id = None
        self.active_label = None
        self.session_name = "NONAME"

        self.latest_meta = data.generate_meta(
            self.session_name, 0, self.measurement_id, self.active_label,
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
                except NameError:
                    previous_meta = self.latest_meta

                # If data saving active, save measurement ID
                try:
                    self.measurement_id += 1
                    logging.info(
                        "Capturing measurement %s with label %s"
                        % (self.measurement_id, self.active_label)
                    )
                except TypeError:
                    pass

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
                    session_name, time_stamp, measurement_id, active_label
                )

                # Wait for all processes to finish
                cloud.join()
                thermal.join()
                camera.join()

                # Shuffle metas
                self.latest_meta = previous_meta
                previous_meta = json.dumps(metadata)

                sleep(float(self.camera_sleep))

        # Start logging thread
        logging_thread = mp.Process(target=thread_function)
        logging_thread.start()

    def start(self, session_name):

        pass

    def stop(self):
        """Stop logging"""

        self.stop_flag = True

        self.chosen_labels = "_"
        self.active_label = "_"
        self.active_model = "_"

        return "success"

    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return self.latest_meta

    def get_temperature_window(self):
        """Returns last 300 temperature readings"""

        return self.temperature_window

    def get_chosen_labels(self):
        """Returns options for labels selected from `all_labels` in new session process"""

        # (Placeholder) TODO: Update to return list of labels that adapts to selected dropdown
        return '[{"ID":"0","label":"discard"},{"ID":"1","label":"water_boiling"},{"ID":"2","label":"water_not_boiling"}]'

    def set_chosen_labels(self, string):
        """Returns options for labels selected from `all_labels` in new session process"""

        self.chosen_labels = string

        self.active_label = str(list(string.split(","))[0])
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

        servo.update_setpoint(value)
        self.hob_setpoint = value

        return "success"

    def set_hob_off(self):
        """Command to turn hob off"""

        servo.hob_off()
        self.hob_setpoint = "OFF"

        return "success"

    def set_camera_sleep(self, value):
        """Command to change camera targe refresh rate"""

        self.camera_sleep = value

        return "success"

    def get_all_labels(self):
        """Returns available image labels for training"""

        data = '[{"ID":"0","label":"discard,water_boiling,water_not_boiling"},{"ID":"1","label":"discard,onions_cooked,onions_not_cooked"}]'

        return data

    def get_all_models(self):
        """Returns available models for prediction"""

        data = '[{"ID":"0","label":"tflite_water_boiling_1"}]'

        return data
