from thermal_camera import THERMAL_CAMERA
from camera import CAMERA
from cloud import CLOUD
from time import sleep 
import datetime
import json

cloud = CLOUD()
thermal = THERMAL_CAMERA(visualise_on=False)
camera = CAMERA()

session_id = "testsession"
measurement_id = 0
time_interval = 1 # in seconds

while True:

    measurement_id += 1
    time_stamp = datetime.datetime.now()

    image_path = camera.capture(cloud.get_path(session_id, "camera", "jpg", time_stamp, measurement_id))
    
    thermal.capture_frame()
    thermal_path = thermal.save_latest_jpg(cloud.get_path(session_id, "thermal", "jpg", time_stamp, measurement_id))
    temperature = thermal.get_latest_temperature()
    
    data = {
        "session_id":session_id,
        "measurement_id":measurement_id,
        "time_stamp":str(time_stamp),
        "temperature":temperature,
        "image_path":image_path,
        "thermal_path":thermal_path
            }
    
    json_path = cloud.get_path(session_id, "meta", "json", time_stamp, measurement_id)
    
    with open(json_path, "w") as write_file:
        json.dump(data, write_file)
    
    cloud.upload_from_filename(image_path)
    cloud.upload_from_filename(thermal_path)
    cloud.upload_from_filename(json_path)
    
    sleep(time_interval)
    

