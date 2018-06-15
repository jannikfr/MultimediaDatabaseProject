import os
import importer
from db_connection import DBConnection

my_db_connection = DBConnection()

refresh_db = False

# Set environment variables
working_dir = os.path.dirname(os.path.realpath(__file__))
path_source = working_dir + "/source/"

# Write images to database
if refresh_db:
    images = importer.import_pictures(path_source)
    for image in images:
        my_db_connection.write_image_to_database(image)





