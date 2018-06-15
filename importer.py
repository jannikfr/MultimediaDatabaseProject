import os
import cv2
from image import Image


def import_pictures(path):

    images = []

    for directory in os.listdir(path):
        subdirectory_path = (path + directory)
        if directory != ".DS_Store":
            for image in os.listdir(subdirectory_path):
                temp_image = Image()
                image_path = subdirectory_path + "/" + image
                temp_image.classification = directory
                temp_image.path = image_path
                temp_image.image = cv2.imread(image_path)
                images.append(temp_image)

    return images





