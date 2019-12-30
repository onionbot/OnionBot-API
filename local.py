# Local 



import logging
import threading
import time

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

        self.config_file_path = "config.txt"
        self._update_config()


    def _update_config(self):

        # Refresh config.txt file 

        self.active_label = 
        self.active_model = 
        self.temperature_setpoint = 
        self.frame_rate = 


    def start(self, session_name, chosen_labels):
        """Start logging"""

        self.session_name = session_name
        self.chosen_labels = chosen_labels

        def thread_function(name):
            """Threaded to run capture loop in background while allowing other processes to continue"""


                session_name = self.session_name
                chosen_labels = self.chosen_labels

            logging.info("Thread %s: starting", name)
            
            while self.stop_flag == False:

                self._update_config()

                print ("Onionlog")

                self.latest_meta = onionbot.capture
                
                time.sleep(1/self.frame_rate)
            
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

        return 1 


    # PARAMETERS STORED IN LOCAL VARIABLE (lost at end of session)

    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return self.latest_meta


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

        return.camera_frame_rate


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


