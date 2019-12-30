# Local 



import logging
import threading
import time


class LOCAL(object):

    def __init__(self):
        
        self.latest_meta = None
        self.stop_flag = False


    def start(self, session_name):
        """Start logging"""

        self.session_name = session_name

        def thread_function(name):

            logging.info("Thread %s: starting", name)
            
            while self.stop_flag is False:

                print ("Onionlog")
                time.sleep(2)
            
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


    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return self.latest_meta

    def get_labels(self):
        """Returns cloud filepath of labels.json - includes available image labels"""

        return local.get_labels()


    def set_active_label(self, string):
        """Command to change current active label -  for building training datasets"""

        local.set_active_label(string)

        return 1


    def get_models(self):
        """Returns cloud filepath of models.json - available models for prediction"""

        return local.get_models()


    def set_active_model(self, string):
        """Command to change current active model for predictions"""

        local.set_active_model(string)

        return 1


    def set_temperature_setpoint(self, value):
        """Command to change current temperature setpoint"""

        local.set_temperature_setpoint(value)

        return 1


    def set_camera_frame_rate(self, value):
        """Command to change camera targe refresh rate"""

        return local.set_camera_frame_rate(value)


local = LOCAL()

local.start("test")


