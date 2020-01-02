import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

import datetime
from google.cloud import storage
client = storage.Client()
# GOTO: https://console.cloud.google.com/storage/browser/[bucket-id]/

bucket_name = 'onionbucket'

bucket=client.get_bucket(bucket_name)

class CLOUD(object):
    """Save image to file"""

    def __init__(self):
        pass
    
    
    def upload_from_filename(self, path):
            blob = bucket.blob(path)
        blob.upload_from_filename(path)
        blob.make_public()
        #print("Uploaded to cloud:", path)
        #print("Blob is publicly accessible at ", blob.public_url) 
        

    def get_path(self, session_name, sensor, file_type, time, measurement_id):
        
        #Make local path
        time_data = time.strftime("%Y-%m-%d_%H-%M-%S-%f")
        path = F"{session_name}/{sensor}"
        filename = F"{session_name}_{str(measurement_id).zfill(5)}_{time_data}_{sensor}.{file_type}"
        os.makedirs(path, exist_ok=True)
        
        return F"{path}/{filename}"
        
        
        
    def get_public_path(self, local_path):
        
        # Public URL 
        cloud_location = "https://storage.googleapis.com/" + bucket_name
        
        return F"{cloud_location}/{local_path}"


