"""Helper functions for generating panoramics."""
import logging
import os
from contextlib import redirect_stderr
from glob import glob
from shutil import copyfile

import cv2
import numpy as np
import psutil
from tqdm import tqdm

logger = logging.getLogger(__name__)


def prepare_directories_for_stitching_in_rows(input_dir):
    """Prepare images for stitching by row.

    Iterates over all images in the input directory, when it sees a black 'stop' image,
    the end of the row is signalled, so all the previous images are added
    to a numbered directory, corresponding to that row.

    Args:
        input_dir (str): input directory of images
    Returns: Nothing. Indexes a side effect.
    """
    image_files = sorted(glob(f'{input_dir}/*JPG'))

    directory_number = 0
    images_in_one_row = []
    debug_logs = []
    for img_name in tqdm(image_files):
        image_pixel_mean = int(np.mean(cv2.imread(img_name)))

        # if we see a black 'end of row' image, copy all previous images to a new numbered directory.
        if image_pixel_mean < 10:
            debug_logs.append((img_name, round(image_pixel_mean, 2)))
            new_dir = f'{input_dir}/row_{str(directory_number).zfill(2)}'
            create_dir_if_needed(new_dir)
            for img_in_row in images_in_one_row:
                copyfile(img_in_row, f'{new_dir}/{img_in_row.split("/")[-1]}')
            images_in_one_row = []
            directory_number += 1
        else:
            images_in_one_row.append(img_name)
    logger.debug(debug_logs)


def stitch_images(image_list):
    """Stitch a list of images together.

    And try to supress OpenCV/MPL std err output...

    Args:
        image_list (list)
    Returns:
        np.ndarray: stitched image
    """
    #  stitch modes: cv2.Stitcher_PANORAMA, cv2.Stitcher_SCANS
    stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    with redirect_stderr('') as _:
        _, stitched = stitcher.stitch(image_list)
    return stitched


def create_dir_if_needed(dir_name):
    """Create directory if needed."""
    if not os.path.isdir(dir_name):
        logger.debug(f'Creating dir: {dir_name}')
        os.mkdir(dir_name)


def get_memory_usage():
    """Returns memory usage of current process in MB. Used for logging.

    Returns:
        float: Memory usage of current process in MB.
    """
    pid = os.getpid()
    return round(psutil.Process(pid).memory_info().rss / 1e6, 2)


def crop_border(img, border_x, border_y):
    """Crop the border of an image. Due to peripheral blurring.

    Args:
        img (np.ndarray): input image
        border_x (int): number of pixels to crop on each side of x border
        border_y (int): number of pixels to crop on each side of y border
    Returns:
        np.ndarray - cropped image
    """
    return img[border_y:-border_y, border_x:-border_x, :]


def sort_jpg_files_in_dir_alpha(in_dir):
    """Alphabetically sort all the jpg files in a directory and return as a list."""
    return sorted(glob(in_dir + '/*JPG'))


def rm_files_in_dir(directory):
    [os.remove(f) for f in glob(f'{directory}*')]
