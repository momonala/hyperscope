import os
from glob import glob

import cv2
import matplotlib.pyplot as plt
import numpy as np
import psutil


def stitch_images(image_list):
    """ Stitch a list of images together.
    Args:
        image_list (list)
    Returns:
        np.ndarray: stitched image
    """
    stitcher = cv2.createStitcher()
    _, stitched = stitcher.stitch(image_list)
    return stitched


def read_image_rgb(img_file):
    """ Read in an image to an np.ndarray into RGB format."""
    return cv2.cvtColor(cv2.imread(img_file), cv2.COLOR_BGR2RGB)


def rotate(img_file):
    """ Rotate an image if needed, clockwise by 90 deg, and overwrite file."""
    img = cv2.imread(img_file)
    if img.shape != (2848, 4288, 3):
        rotated = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(img_file, rotated)


def bgr2rgb(bgr):
    """ Convert np.ndarray BGR image to RGB."""
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def crop_border(img, border_x, border_y):
    """ Crop the border of an image. Due to peripheral blurring.

        Args:
            img (np.ndarray): input image
            border_x (int): number of pixels to crop on each side of x border
            border_y (int): number of pixels to crop on each side of y border
        Returns:
            np.ndarray - cropped image
    """
    return img[border_y:-border_y, border_x:-border_x, :]


def plot(img):
    """ Plot an image. """
    plt.imshow(img)
    plt.show()


def get_mag(img):
    """ Get magnitude (energy) of image. """
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
    mag = np.mean(np.sqrt(sobelx ** 2 + sobely ** 2))
    return mag


def rm_files_in_dir(directory):
    [os.remove(f) for f in glob(f'{directory}*')]


def get_memory_usage():
    """ Returns memory usage of current process in MB. Used for logging.

    Returns:
        float: Memory usage of current process in MB.
    """
    pid = os.getpid()
    return round(psutil.Process(pid).memory_info().rss / 1e6, 2)
