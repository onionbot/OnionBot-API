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



INITIAL_META = {
              "type": "meta",
                "id": "pre_start",
                "attributes": {
                    "session_name": "Initialising...",
                    "label": "Initialising...",
                    "camera_prediction": "Initialising...",
                    "thermal_prediction": "Initialising...",
                    "measurement_id": "Initialising...",
                    "time_stamp": "Initialising...",
                    "temperature": "Initialising...",
                    "camera_filepath": "placeholder.png",
                    "thermal_filepath": "placeholder.png",
                    "hob_setpoint": "Initialising...",
                    "camera_sleep": "Initialising...",
                },
              }
    
               


class LOCAL(object):

    def __init__(self):
        

        self.latest_meta = json.dumps(INITIAL_META)
        self.stop_flag = False
        
        self.chosen_labels = "_"
        self.active_label = "discard"
        self.active_model = "_"
        
        self.camera_sleep = "0"
        self.hob_setpoint = " 100"


    def start(self, session_name):
        """Start logging"""

        self.session_name = session_name

        def thread_function(name):
            """Threaded to run capture loop in background while allowing other processes to continue"""


            def capture(measurement_id):
                """Subfunction to capture sensor data"""

                # Start timer
                time_stamp = datetime.datetime.now()
                
                # Capture sensor data 
                camera_filepath = camera.capture(cloud.get_path(self.session_name, "camera", "jpg", time_stamp, measurement_id, self.active_label))
                thermal.capture_frame()
                thermal_filepath = thermal.save_latest_jpg(cloud.get_path(self.session_name, "thermal", "jpg", time_stamp, measurement_id, self.active_label))
                temperature = thermal.get_latest_temperature()
                
                # Upload to cloud
                cloud.upload_from_filename(camera_filepath)
                cloud.upload_from_filename(thermal_filepath)

                # Make prediction based on specified deep learning model
                
                camera_prediction = "_aaa"
                thermal_prediction = "_aaaa"

                # Generate metadata
   
                data = {
                  "type": "meta",
                    "id": F"{session_name}_{measurement_id}_{str(time_stamp)}",
                    "attributes": {
                        "session_name": session_name,
                        "active_label": self.active_label,
                        "active_model": self.active_model,
                        "camera_prediction": camera_prediction,
                        "thermal_prediction": thermal_prediction,
                        "measurement_id": measurement_id,
                        "time_stamp": str(time_stamp),
                        "temperature": str(temperature),
                        "camera_filepath": cloud.get_public_path(camera_filepath),
                        "thermal_filepath": cloud.get_public_path(thermal_filepath),
                        "hob_setpoint": self.hob_setpoint,
                        "camera_sleep": self.camera_sleep,
                    },
                  }
                
                json_filepath = cloud.get_path(self.session_name, "meta", "json", time_stamp, measurement_id, self.active_label)
                with open(json_filepath, "w") as write_file:
                    json.dump(data, write_file)
                
                # Upload to cloud
                cloud.upload_from_filename(json_filepath)
                
                return json.dumps(data)




            logging.info("Thread %s: starting", name)
            measurement_id = 0

            # WHILE LOOP
            
            while self.stop_flag == False:
                
                measurement_id += 1
                
                print (F"Capturing measurement {measurement_id} with label {self.active_label}")
                
                self.latest_meta = capture(measurement_id)
                
                sleep(float(self.camera_sleep))
            
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


        return "success"


    def stop(self):
        """Stop logging"""

        self.stop_flag = True

        self.latest_meta = json.dumps(INITIAL_META)
        self.chosen_labels = "_"
        self.active_label = "_"
        self.active_model = "_"

        return "success" 


    # PARAMETERS STORED IN LOCAL VARIABLE (lost at end of session)

    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return self.latest_meta


    def get_chosen_labels(self):
        """Returns options for labels selected from `all_labels` in new session process"""
        
#         chosen_labels = self.chosen_labels
#         label_list = str(list(chosen_labels.split(",")))
#         custom_json = 
#         
#         output = ""
#         for n in length(label_list):
#             label = F'{"ID:"{n}","label":{label_list[0]"'
#             output = output + label
#         
#         {"ID":"0","label":"discard,water_boiling,water_not_boiling"}


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

        self.active_model = string
        return "success"


    # PARAMETERS STORED IN CONFIG FILE (saved after each session on pi)



    def set_hob_setpoint(self, value):
        """Command to change current temperature setpoint"""
        
        self.hob_setpoint = value
        
        # val = float(val) 
        # send command to hob to set         
        
        return "success"


    def set_camera_sleep(self, value):
        """Command to change camera targe refresh rate"""

        self.camera_sleep = value
        
        return "success"


    # PARAMETERS STORED IN TEXT FILES (retrieve hard copies)

    def get_all_labels(self):
        """Returns available image labels for training"""

        data = '[{"ID":"0","label":"discard,water_boiling,water_not_boiling"},{"ID":"1","label":"discard,onions_cooked,onions_not_cooked"}]'
        
        return data 


    def get_all_models(self):
        """Returns available models for prediction"""
        
        data = '[{"ID":"0","label":"test_model"}]'
        
        return data
    
#local = LOCAL()
#local.start('test')
