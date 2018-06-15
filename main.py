import json

import cv2
import os
import importer

working_dir = os.path.dirname(os.path.realpath(__file__))
path_source = working_dir + "/source/"

images = importer.import_pictures(path_source)
print(len(images))

export_file_json = open(os.path.join(working_dir, "mmdbs.json"), "wt")


export_data = []
for image in images:
    image_data = {"classification": image.classification, "path": image.path}
    export_data.append(image_data)


export_file_json.write(json.dumps(export_data))
export_file_json.close()  # Close the file
