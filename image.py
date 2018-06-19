import numpy
import cv2


class Image:
    def __init__(self):
        self.classification = ""
        self.image = numpy.empty
        self.sobel_edge_detection = numpy.empty
        self.path = ""
        self.global_edge_histogram = {}
        self.local_histogram = {}
        self.global_histogram = {}
