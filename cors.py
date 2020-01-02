import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/onionbot-819a387e4e79.json"

from google.cloud import storage
client = storage.Client()
# GOTO: https://console.cloud.google.com/storage/browser/[bucket-id]/

bucket_name = 'onionbucket'

bucket=client.get_bucket(bucket_name)


policies = []
# policies.extend([
#             {'origin': ['http://localhost:8888']},
#             {'method': ['GET']},
#             {'responseHeader': ['Content-Type']},
#             {'maxAgeSeconds': 3600}
#         ])
# policies = '[ { "origin": ["http://localhost:8888"], "responseHeader": ["Content-Type"], "method": ["GET"], "maxAgeSeconds": 3600 } ]'

bucket.cors = policies
bucket.update()
print("__________________________", bucket.cors)

