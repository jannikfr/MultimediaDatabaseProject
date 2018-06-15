import numpy
import cv2


class Image:
    def __init__(self):
        self.classification = ""
        self.image = numpy.empty
        self.path = ""
        self.local_histogram = {}
        self.global_histogram = {}
