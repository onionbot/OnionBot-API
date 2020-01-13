from os import walk
import csv
import json


session_ID = "monday1_backup"
path = F"/Users/bencobley/Downloads/{session_ID}/meta_flat"
csv_file = F"/Users/bencobley/Downloads/{session_ID}/temperature_time_series.csv"


files = []
directories = []
for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break

filenames = [file for file in filenames if file.endswith(".json")]

with open(csv_file, mode='w') as temperature_file:
    file_writer = csv.writer(temperature_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for filename in filenames:
        print (filename)
        with open(F"{path}/{filename}") as jsonfile:
            data = json.load(jsonfile)
            attributes = data['attributes']
            file_writer.writerow([str(attributes['time_stamp']),str(attributes['active_label']),str((attributes['temperature'])) ])



