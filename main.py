import collections
import math
import numpy as np

import cv2
import os
import feature_extractor
import db_connection
from image import Image

refresh_db = True

# Set environment variables
working_dir = os.path.dirname(os.path.realpath(__file__))
path = working_dir + "/source/"
print("Working directory is " + working_dir + ".")
print("The images are stored in " + path + ".")

# Establish DB connection
conn = db_connection.connect()

# Loop trough all subdirectories of the given path if refresh = TRUE
# The name of each subdirectory represents the class of the images inside
if refresh_db:

    # Clean up database.
    print("Clean up database.")
    number_of_deleted_images = db_connection.delete_all_images(conn)
    print(str(number_of_deleted_images) + " images deleted in database.")

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

                # Convert to HSV color space
                temp_image.image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2HSV)
                # temp_image.image = cv2.normalize(temp_image.image, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

                temp_image.local_histogram = feature_extractor.extract_histograms(temp_image.image, 1, 2, [8, 2, 4],
                                                                                  False)
                temp_image.global_histogram = feature_extractor.extract_histograms(temp_image.image, 1, 1, [8, 2, 4],
                                                                                   False)

                temp_image.sobel_edge_detection = feature_extractor.sobel_edge_detection(temp_image.image)
                temp_image.global_edge_histogram = feature_extractor.extract_histograms_greyscale(
                    temp_image.sobel_edge_detection, 1, 1, 64, False, np.min(temp_image.sobel_edge_detection),
                    np.max(temp_image.sobel_edge_detection))

                # See outputs
                # cv2.imwrite(image, temp_image.sobel_edge_detection)
                # print(temp_image.global_edge_histogram)

                # Write the features of the Image object to the database
                db_connection.write_image_to_database(conn, temp_image)

# Close database connection
db_connection.close_connection(conn)
