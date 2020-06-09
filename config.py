from json import dumps, dump, load

FILE = "/home/pi/onionbot/config.json"


class Settings(object):
    """Interface with the `config.json` settings dictionary"""

    def get_setting(self, key):

        with open(FILE) as json_data_file:
            config = load(json_data_file)

            settings = config["settings"]

            try:
                return settings[key]
            except KeyError:
                raise KeyError("Settings key not found")

    def set_setting(self, key, value):

        with open(FILE) as json_data_file:
            config = load(json_data_file)

            settings = config["settings"]

        if key in settings:
            settings[key] = value
            config["settings"] = settings

            # dump new version of config
            with open(FILE, "w") as outfile:
                dump(config, outfile, indent=4)
        else:
            raise KeyError("Settings key not found")


class Labels(object):
    """Interface with the `config.json` labels dictionary"""

    def get_labels(self):

        with open(FILE) as json_data_file:
            config = load(json_data_file)
            labels = config["labels"]
            return dumps(labels)


class Classifiers(object):
    """Interface with the `config.json` classifiers dictionary"""

    def get_classifiers(self):

        with open(FILE) as json_data_file:
            config = load(json_data_file)
            classifiers = config["classifiers"]
            return classifiers
