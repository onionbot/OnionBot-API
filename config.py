class Config(object):

    def __init__(self):

        self.camera_sleep = 0

        self.config_file = {"camera_sleep": 0}

    def get_config(self, key):

        try:
            return self.config_file[key]
        except KeyError:
            raise KeyError("Config key not found")  

    def set_config(self, key, value):

        if key in self.config_file:
            self.config_file[key] = value
        else:
            raise KeyError("Config key not found")  
