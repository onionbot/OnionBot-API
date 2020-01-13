from os import walk
import csv


session_ID = "monday1"
sensor = "camera"
label = "not_boiling"
path = F"/Users/bencobley/Downloads/{session_ID}/{sensor}/{label}"
csv_file = F"/Users/bencobley/Downloads/{session_ID}/{sensor}_{label}.csv"


files = []
directories = []
for (dirpath, dirnames, filenames) in walk(path):
    files.extend(filenames)
    break



total_count = 0
skip_count = 0
added_count = 0 

with open(csv_file, mode='w') as label_file:
    file_writer = csv.writer(label_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    file_writer.writerow(["image_path[,label]"])
    
    for filename in filenames:
        total_count += 1
        skip_count += 1
        if skip_count == 4: 
            file_writer.writerow([str(F"gs://onionbucket/logs/{session_ID}/{sensor}/{label}/{filename},{label}")])
            skip_count = 0
            added_count += 1


print (F"Added {added_count} files to csv")

