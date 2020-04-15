import json
from cloud import Cloud

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

        self.camera_filepath = cloud.get_path(
            session_name=session_name,
            sensor="camera",
            file_type="jpg",
            time=time_stamp,
            measurement_id=measurement_id,
            label=active_label,
        )

        self.thermal_filepath = cloud.get_path(
            session_name=session_name,
            sensor="thermal",
            file_type="jpg",
            time=time_stamp,
            measurement_id=measurement_id,
            label=active_label,
        )

        self.thermal_history_filepath = cloud.get_path(
            session_name=session_name,
            sensor="thermal_history",
            file_type="json",
            time=time_stamp,
            measurement_id=measurement_id,
            label=active_label,
        )

        self.meta_filepath = cloud.get_path(
            session_name=session_name,
            sensor="meta",
            file_type="json",
            time=time_stamp,
            measurement_id=measurement_id,
            label=active_label,
        )

        return (
            self.camera_filepath,
            self.thermal_filepath,
            self.thermal_history_filepath,
        )

    def generate_meta(
        self, session_name, time_stamp, measurement_id, active_label, hob_setpoint
    ):
        """Generate metadata to be parsed by portal / training process"""

        data = {
            "type": "meta",
            "id": f"{session_name}_{measurement_id}_{str(time_stamp)}",
            "attributes": {
                "session_name": session_name,
                "active_label": active_label,
                "measurement_id": measurement_id,
                "time_stamp": str(time_stamp),
                "camera_filepath": cloud.get_public_path(self.camera_filepath),
                "thermal_filepath": cloud.get_public_path(self.thermal_filepath),
                "thermal_history_filepath": cloud.get_public_path(
                    self.thermal_history_filepath
                ),
                "hob_setpoint": str(hob_setpoint),
            },
        }

        # Remove dictionary elements with 'None' type
        attributes = data.get("attributes")
        cleaned_data = {
            key: value for key, value in attributes.items() if value is not None
        }
        cleaned_data = {"attributes": cleaned_data}
        data.update(cleaned_data)

        if self.meta_filepath:
            with open(self.meta_filepath, "w") as write_file:
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







