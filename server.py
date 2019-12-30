""" Server - handles communication with 'local' Pi device - currently also running on Pi but 
designed as a passthrough with future proofing in mind, could be run on Python backend"""

import local


class SERVER(object):

    def __init__(self):
        """Cloud-server-to-pi communication could be initiated here, 
        in future if running in cloud"""
        pass


    def start(self, session_name):
        """Sends start command to Pi"""

        return local.start(session_name)


    def stop(self):
        """Sends stop command to Pi"""

        return local.stop()


    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return local.get_latest_meta


    def get_labels(self):
        """Returns cloud filepath of labels.json - includes available image labels"""

        return local.get_labels()


    def set_active_label(self, string):
        """Command to change current active label -  for building training datasets"""

        return local.set_active_label(string)


    def get_models(self):
        """Returns cloud filepath of models.json - available models for prediction"""

        return local.get_models()


    def set_active_model(self, string):
        """Command to change current active model for predictions"""

        return local.set_active_model(string)


    def set_temperature_setpoint(self, value):
        """Command to change current temperature setpoint"""

        return local.set_temperature_setpoint(value)


    def set_camera_frame_rate(self, value):
        """Command to change camera targe refresh rate"""

        return local.set_camera_frame_rate(value)


