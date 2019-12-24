import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

import datetime
from google.cloud import storage
client = storage.Client()
# GOTO: https://console.cloud.google.com/storage/browser/[bucket-id]/

bucket=client.get_bucket('onionbucket')

class CLOUD(object):
    """Save image to file"""

    def __init__(self):
        pass
    
    
    def upload(self, path):
        blob = bucket.blob(path)
        blob.upload_from_filename(path)
        print("Uploaded to cloud:", path)


    def get_path(self, session_name, sensor, file_type, time):
        
        time_data = time.strftime("%Y-%m-%d_%H-%M-%S-%f")
        path = "logs/%s/%s" % (session_name, sensor)
        filename = "%s_%s_%s.%s" % (session_name, time_data, sensor, file_type)
        
        os.makedirs(path, exist_ok=True)
        return"%s/%s" % (path, filename)
