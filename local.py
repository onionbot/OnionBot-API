# Local 



import cloud etc


class LOCAL(object):

    def __init__(self):
        pass


    def start(self):
        """Sends start command to Pi"""


        return 1


    def stop(self):
        """Sends stop command to Pi"""


        return 1 


    def get_latest_meta(self):
        """Returns cloud filepath of latest meta.json - includes path location of images"""



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