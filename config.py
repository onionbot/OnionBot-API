import json


class Config(object):

    def __init__(self, file):
        self.file = file

    def get_config(self, key):

        with open(self.file) as json_data_file:
            config = json.load(json_data_file)
            try:
                return config[key]
            except KeyError:
                raise KeyError("Config key not found")

    def set_config(self, key, value):

        with open(self.file) as json_data_file:
            config = json.load(json_data_file)

            if key in config:
                config[key] = value

                # Close file then dump new version of config
                json_data_file.close()
                with open("config.json", "w") as outfile:
                    json.dump(config, outfile)
            else:
                raise KeyError("Config key not found")
