import math

import numpy as np
import collections
import cv2


def extract_histograms(image_param, h_splits, v_splits, number_of_bins, show_cells):
    """
    Split a given image in equal sized cells corresponding to the given number of vertical and horizontal splits,
    e.g. v_splits = 2 and h_splits=3 results in 6 cells. For each cell a histogram is computed whereby the colors are
    binned corresponding to the parameter number_of_bins.
    :param image_param: Image whose histograms need to be computed. Assumes normal cv2 color ranges.
    :param h_splits: The number of horizontal splits.
    :param v_splits: The number of vertical splits.
    :param number_of_bins: The number of bins for grouping the subcolor spaced h, s, v
    :param show_cells: If True, the cells are displayed in an external window for 5 seconds each.
    :return: A dictionary containing the h_splits, v_splits, the number_of_splits and the histogram for each cell.
    """

    # Add additional information about histogram computation to the return value
    histogram = {}
    histogram['h_splits'] = h_splits
    histogram['v_splits'] = v_splits
    histogram['number_of_bins (h,s,v)'] = number_of_bins
    histogram['cell_histograms'] = []

    # Split along horizontal axis
    horizontal_split_images = np.split(image_param, h_splits, axis=0)
    for hor_index, horizontal_split_image in enumerate(horizontal_split_images):

        # Loop over split sub images and split each along vertical axis
        horizontal_vertical_split_images = np.split(horizontal_split_image, v_splits, axis=1)
        for ver_index, horizontal_vertical_split_image in enumerate(horizontal_vertical_split_images):

            # Display the cells if desired in parameter
            if show_cells:
                cv2.imshow("Current cell: hor:" + hor_index + "/ver: " + ver_index,
                           cv2.cvtColor(horizontal_vertical_split_image, cv2.COLOR_HSV2BGR))
                cv2.waitKey(5000)

            # Create empty dictonary and add information about histogram of this cell
            cell_histogram = {'horizontal_index': hor_index, 'vertical_index': ver_index}

            h = 0
            s = 0
            v = 0

            # Loop over each value in pixel and assign bin to the h, s and v values
            for (x, y, z), value in np.ndenumerate(horizontal_vertical_split_image):

                if z == 0:
                    h = int(value / (180 / number_of_bins[z]))
                elif z == 1:
                    s = int(value / (256 / number_of_bins[z]))
                elif z == 2:
                    v = int(value / (256 / number_of_bins[z]))

                    # Build String key in dictionary since needs a String for saving into db
                    key = str(h) + "," + str(s) + "," + str(v)

                    # All values for this pixel are processed
                    # Build key to compute new binned HSV value
                    # Increase the counter for this HSV value if exists
                    if key in cell_histogram:
                        cell_histogram[key] = cell_histogram[key] + 1
                    # HSV value does not exist yet => create it and set counter to 1
                    else:
                        cell_histogram[key] = 1

                    # Reset variables
                    h = 0
                    s = 0
                    v = 0

            # Order dictonary and append it to the overall dictionary
            # cell_histogram = collections.OrderedDict(sorted(cell_histogram.items()))
            histogram['cell_histograms'].append(cell_histogram)

    return histogram


def sobel_edge_detection(image_param):
    input_image = cv2.cvtColor(image_param, cv2.COLOR_BGR2GRAY)

    kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, - 1]], dtype=np.float)

    v_kernel = kernel
    h_kernel = np.transpose(kernel)

    N = input_image.shape[0]  # row
    M = input_image.shape[1]  # column

    output = np.zeros((N, M))

    # Surrounds array with 0's on the outside perimeter
    input_image = np.pad(input_image, pad_width=1, mode='constant', constant_values=0)

    for i in range(1, N - 1):
        for j in range(1, M - 1):
            sub_input = input_image[(i - 1):(i + 2), (j - 1):(j + 2)]

            h_gradient = np.sum(np.multiply(sub_input, h_kernel))
            v_gradient = np.sum(np.multiply(sub_input, v_kernel))

            # Calculate the gradient magnitude
            output[i - 1][j - 1] = math.sqrt(h_gradient * h_gradient + v_gradient * v_gradient)

    return output


def extract_histograms_greyscale(image_param, h_splits, v_splits, number_of_bins, show_cells, min_value, max_value):
    """
    Split a given greyscale image in equal sized cells corresponding to the given number of vertical and horizontal splits,
    e.g. v_splits = 2 and h_splits=3 results in 6 cells. For each cell a histogram is computed whereby the colors are
    binned corresponding to the parameter number_of_bins.
    :param image_param: Greyscale image whose histograms need to be computed
    :param h_splits: The number of horizontal splits.
    :param v_splits: The number of vertical splits.
    :param number_of_bins: The number of bins for grouping the greyscale range
    :param show_cells: If True, the cells are displayed in an external window for 5 seconds each.
    :param min_value: Smallest value of the color range. Needed for normalization.
    :param max_value: Greatest value of the color range. Needed for normalization.
    :return: A dictionary containing the h_splits, v_splits, the number_of_splits and the histogram for each cell.
    """

    # Add additional information about histogram computation to the return value
    histogram = {}
    histogram['h_splits'] = h_splits
    histogram['v_splits'] = v_splits
    histogram['number_of_bins'] = number_of_bins
    histogram['cell_histograms'] = []

    # Split along horizontal axis
    horizontal_split_images = np.split(image_param, h_splits, axis=0)
    for hor_index, horizontal_split_image in enumerate(horizontal_split_images):

        # Loop over split sub images and split each along vertical axis
        horizontal_vertical_split_images = np.split(horizontal_split_image, v_splits, axis=1)
        for ver_index, horizontal_vertical_split_image in enumerate(horizontal_vertical_split_images):

            # Display the cells if desired in parameter
            if show_cells:
                cv2.imshow("Current cell: hor:" + hor_index + "/ver: " + ver_index, horizontal_vertical_split_image)
                cv2.waitKey(5000)

            # Create empty dictonary and add information about histogram of this cell
            cell_histogram = {'horizontal_index': hor_index, 'vertical_index': ver_index}

            # Loop over each value in pixel and assign bin to the h, s and v values
            for (x, y), value in np.ndenumerate(horizontal_vertical_split_image):

                normalized_value = (value - min_value) / (max_value - min_value)
                bin = int(normalized_value * number_of_bins)

                # Increase the counter for this bin if exists
                if bin in cell_histogram:
                    cell_histogram[bin] = cell_histogram[bin] + 1
                # HSV value does not exist yet => create it and set counter to 1
                else:
                    cell_histogram[bin] = 1

            # Order dictonary and append it to the overall dictionary
            # cell_histogram = collections.OrderedDict(sorted(cell_histogram.items()))
            histogram['cell_histograms'].append(cell_histogram)

    return histogram
