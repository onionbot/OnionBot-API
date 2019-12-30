# Local 



import logging
import threading
import time
from time import sleep

from thermal_camera import THERMAL_CAMERA
from camera import CAMERA
from cloud import CLOUD

import datetime
import json

cloud = CLOUD()
thermal = THERMAL_CAMERA(visualise_on=False)
camera = CAMERA()


class LOCAL(object):

    def __init__(self):
        
        self.latest_meta = None
        self.stop_flag = False
        
        self.latest_meta = None
        self.chosen_labels = None
        self.active_label = None
        self.active_model = None
        
        self.camera_frame_rate = 1
        self.temperature_set_point = 1


    def start(self, session_name):
        """Start logging"""

        self.session_name = session_name
        self.bucket_name = cloud.bucket_name

        def thread_function(name):
            """Threaded to run capture loop in background while allowing other processes to continue"""


            def capture(measurement_id):
                """Subfunction to capture sensor data"""

                # Start timer
                time_stamp = datetime.datetime.now()

                # Update variables
                session_name = self.session_name
                label = self.active_label
                model = self.set_active_model
                
                # Capture sensor data 
                image_filepath = camera.capture(cloud.get_path(session_name, "camera", "jpg", time_stamp, measurement_id))
                thermal.capture_frame()
                thermal_filepath = thermal.save_latest_jpg(cloud.get_path(session_name, "thermal", "jpg", time_stamp, measurement_id))
                temperature = thermal.get_latest_temperature()
                
                # Upload to cloud
                cloud.upload_from_filename(image_filepath)
                cloud.upload_from_filename(thermal_filepath)

                # Make prediction based on specified deep learning model
                prediction = "None"

                # Generate metadata
                data = {
                    "session_name":session_name,
                    "label":label,
                    "prediction":prediction,
                    "measurement_id":measurement_id,
                    "time_stamp":str(time_stamp),
                    "temperature":temperature,
                    "image_filepath":self.bucket_name+"/"+image_filepath,
                    "thermal_filepath":self.bucket_name+"/"+thermal_filepath
                        }
                json_filepath = cloud.get_path(session_name, "meta", "json", time_stamp, measurement_id)
                with open(json_filepath, "w") as write_file:
                    json.dump(data, write_file)
                
                # Upload to cloud
                cloud.upload_from_filename(json_filepath)
                
                return json_filepath




            logging.info("Thread %s: starting", name)
            measurement_id = 0

            # WHILE LOOP
            
            while self.stop_flag == False:

                print ("Capturing measurement {measurement_id}")

                measurement_id += 1
                self.latest_meta = capture(measurement_id)
                
                sleep(1/self.camera_frame_rate)
            
            logging.info("Thread %s: finishing", name)
        

        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")       
        
        logging.info("Main    : before creating thread")
        my_thread = threading.Thread(target=thread_function, args=(1,))
        logging.info("Main    : before running thread")
        my_thread.start()
        logging.info("Main    : wait for the thread to finish")
        my_thread.join()
        logging.info("Main    : all done")


        return 1


    def stop(self):
        """Stop logging"""

        self.stop_flag = True

        self.latest_meta = None
        self.chosen_labels = None
        self.active_label = None
        self.active_model = None

        return 1 


    # PARAMETERS STORED IN LOCAL VARIABLE (lost at end of session)

    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return self.latest_meta


    def get_chosen_labels(self):
        """Returns options for labels selected from `all_labels` in new session process"""

        return self.chosen_labels

    
    def set_chosen_labels(self, string):
        """Returns options for labels selected from `all_labels` in new session process"""

        self.chosen_labels = string
        return 1


    def set_active_label(self, string):
        """Command to change current active label -  for building training datasets"""

        self.active_label = string
        return 1


    def set_active_model(self, string):
        """Command to change current active model for predictions"""

        self.active_model = string
        return 1


    # PARAMETERS STORED IN CONFIG FILE (saved after each session on pi)

    def get_temperature_setpoint(self):
        """Command to change current temperature setpoint"""

        return self.temperature_setpoint


    def get_camera_frame_rate(self):
        """Command to change camera targe refresh rate"""

        return self.camera_frame_rate


    def set_temperature_setpoint(self, value):
        """Command to change current temperature setpoint"""

        self.temperature_setpoint = value
        return 1


    def set_camera_frame_rate(self, value):
        """Command to change camera targe refresh rate"""

        self.camera_frame_rate = value
        return 1


    # PARAMETERS STORED IN TEXT FILES (retrieve hard copies)

    def get_all_labels(self):
        """Returns available image labels for training"""

        return self.all_labels


    def get_all_models(self):
        """Returns available models for prediction"""

        return self.all_models


local = LOCAL()

local.start("test")


