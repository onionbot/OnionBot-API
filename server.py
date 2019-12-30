""" Server - handles communication with 'local' Pi device - currently also running on Pi but 
designed as a passthrough with future proofing in mind, could be run on web hosted Python backend"""

import local


class SERVER(object):

    def __init__(self):
        """Cloud-server-to-pi communication could be initiated here, 
        in future if running in cloud"""
        pass


    def start(self, session_name, chosen_labels):
        """Sends start command to Pi"""

        return local.start(session_name), chosen_labels


    def stop(self):
        """Sends stop command to Pi"""

        return local.stop()


    # PARAMETERS STORED IN LOCAL VARIABLES ON PI (lost at end of session)

    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""

        return local.get_latest_meta()


    def get_chosen_labels(self):


    def set_active_label(self, string):
        """Command to change current active label -  for building training datasets"""

        return local.set_active_label(string)


    def set_active_model(self, string):
        """Command to change current active model for predictions"""

        return local.set_active_model(string)


    # PARAMETERS STORED IN CONFIG FILE ON PI (saved after each session on pi)


    def get_temperature_setpoint(self, value):
        """Command to change current temperature setpoint"""

        return local.get_temperature_setpoint()


    def get_camera_frame_rate(self, value):
        """Command to change camera targe refresh rate"""

        return local.get_camera_frame_rate()


    def set_temperature_setpoint(self, value):
        """Command to change current temperature setpoint"""

        return local.set_temperature_setpoint(value)


    def set_camera_frame_rate(self, value):
        """Command to change camera targe refresh rate"""

        return local.set_camera_frame_rate(value)


    # PARAMETERS STORED IN TEXT FILES ON PI (retrieve hard copies on pi)

    def get_all_labels(self):
        """Returns available image labels for training"""

        return local.get_all_labels()


    def get_all_models(self):
        """Returns available models for prediction"""

        return local.get_all_models()





