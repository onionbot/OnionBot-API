import json

FILE = "/home/pi/onionbot/config.json"


class Settings(object):
    def get_config(self, key):

        with open(FILE) as json_data_file:
            config = json.load(json_data_file)

            settings = config["settings"]

            try:
                return settings[key]
            except KeyError:
                raise KeyError("Settings key not found")

    def set_config(self, key, value):

        with open(FILE) as json_data_file:
            config = json.load(json_data_file)

            settings = config["settings"]

        if key in settings:
            settings[key] = value
            config["settings"] = settings

            # dump new version of config
            with open(FILE, "w") as outfile:
                json.dump(config, outfile)
        else:
            raise KeyError("Settings key not found")
