import cv2
import os
import feature_extractor
import db_connection
from image import Image

refresh_db = False

# Set environment variables
working_dir = os.path.dirname(os.path.realpath(__file__))
path = working_dir + "/source/"
print("Working directory is " + working_dir + ".")
print("The images are stored in " + path + ".")


# Establish DB connection
conn = db_connection.connect()

# Loop trough all subdirectories of the given path
# The name of each subdirectory represents the class of the images inside
for subdirectory in os.listdir(path):

    # Build absolute subdirectory path
    subdirectory_path = (path + subdirectory)

    # Ignore files for the MacOS file system
    if subdirectory != ".DS_Store":
        for image in os.listdir(subdirectory_path):

            # Create Image object
            temp_image = Image()

            # Compute features and assign the to the object's attribute
            image_path = subdirectory_path + "/" + image
            temp_image.classification = subdirectory
            temp_image.path = image_path
            temp_image.image = cv2.imread(image_path)

            # Write the features of the Image object to the database
            db_connection.write_image_to_database(conn, temp_image)

# Close database connection
db_connection.close_connection(conn)




