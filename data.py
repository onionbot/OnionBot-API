import json
from cloud import Cloud
import os

import logging

logger = logging.getLogger(__name__)

cloud = Cloud()


class Data:
    def __init__(self):
        self.camera_filepath = None
        self.thermal_filepath = None
        self.thermal_history_filepath = None
        self.meta_filepath = None

    def generate_filepaths(
        self, session_name, time_stamp, measurement_id, active_label
    ):
        """Generate filepaths for local and cloud storage for all file types"""

        filepaths = {}

        path = f"~/onionbot/logs/{session_name}/camera/{active_label}"
        os.makedirs(path, exist_ok=True)
        filename = f"{session_name}_{str(measurement_id).zfill(5)}_{time_stamp}_camera_{active_label}.jpg"
        filepaths["camera"] = f"{path}/{filename}"

        path = f"~/onionbot/logs/{session_name}/thermal/{active_label}"
        os.makedirs(path, exist_ok=True)
        filename = f"{session_name}_{str(measurement_id).zfill(5)}_{time_stamp}_thermal_{active_label}.jpg"
        filepaths["thermal"] = f"{path}/{filename}"

        path = f"~/onionbot/logs/{session_name}/meta/{active_label}"
        os.makedirs(path, exist_ok=True)
        filename = f"{session_name}_{str(measurement_id).zfill(5)}_{time_stamp}_meta_{active_label}.json"
        filepaths["meta"] = f"{path}/{filename}"

        return filepaths

    def generate_meta(
        self,
        session_name,
        time_stamp,
        measurement_id,
        active_label,
        filepaths,
        thermal_data,
        control_data,
    ):
        """Generate metadata to be parsed by portal"""

        camera_filepath = cloud.get_public_path(filepaths["camera"])
        thermal_filepath = cloud.get_public_path(filepaths["thermal"])

        data = {
            "type": "meta",
            "id": f"{session_name}_{measurement_id}_{str(time_stamp)}",
            "attributes": {
                "session_name": session_name,
                "active_label": active_label,
                "measurement_id": measurement_id,
                "time_stamp": time_stamp,
                "camera_filepath": camera_filepath,
                "thermal_filepath": thermal_filepath,
                "temperature": thermal_data["temperature"],
                "thermal_history": thermal_data["thermal_history"],
                "variance": thermal_data["variance"],
                "servo_setpoint": control_data["servo_setpoint"],
                "servo_setpoint_history": control_data["servo_setpoint_history"],
                "servo_achieved": control_data["servo_achieved"],
                "servo_achieved_history": control_data["servo_achieved_history"],
                "temperature_target": control_data["temperature_target"],
                "p_coefficient": control_data["p_coefficient"],
                "i_coefficient": control_data["i_coefficient"],
                "d_coefficient": control_data["d_coefficient"],
            },
        }

        # Remove dictionary elements with 'None' type
        attributes = data.get("attributes")
        cleaned_data = {
            key: value for key, value in attributes.items() if value is not None
        }
        cleaned_data = {"attributes": cleaned_data}
        data.update(cleaned_data)

        logger.debug(data)

        with open(filepaths["meta"], "w") as write_file:
            json.dump(data, write_file)

        return data

    def generate_labels(self):
        """Generate labels for live labelling functionality"""

        data = {
            "type": "labels",
            "attributes": {
                "Onion": {
                    "0": "Discard",
                    "1": "Raw",
                    "2": "Browning",
                    "3": "Brown",
                    "4": "Overcooked",
                },
                "Water": {
                    "0": "Discard",
                    "1": "Not boiling",
                    "2": "Simmering",
                    "3": "Boiling",
                },
            },
        }

        return data
