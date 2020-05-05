import json

SHUTDOWN_FILE = "shutdown.json"


class Shutdown(object):
    def get_shutdown(self, key):

        with open(SHUTDOWN_FILE) as json_data_file:
            shutdown = json.load(json_data_file)
            try:
                return shutdown[key]
            except KeyError:
                raise KeyError("Config key not found")

    def set_shutdown(self, key, value):

        with open(SHUTDOWN_FILE) as json_data_file:
            shutdown = json.load(json_data_file)

            if key in shutdown:
                shutdown[key] = value

                # Close file then dump new version of shutdown
                json_data_file.close()
                with open("shutdown.json", "w") as outfile:
                    json.dump(shutdown, outfile)
            else:
                raise KeyError("Config key not found")
