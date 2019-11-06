"""The OpenCV Panoramic Stitching Algorithms."""

import logging
from glob import glob
import os
import cv2
from tqdm import tqdm

from python_hyperscope.utils import (crop_border,
                                     rm_files_in_dir,
                                     stitch_images,
                                     create_save_dir_if_needed)

logger = logging.getLogger(__name__)


def stitch_images_in_dir(in_dir, save_name):
    """Stitch Images in batches, growing at each function call.

    Args:
        in_dir (str): input directory of images to batch and stitch
        save_name (str): output file name for temporary panoramics

    Returns: Nothing. Creates Pano in microscope_images_processed/tmp_panoX/ directories as a side effect.
    """
    logger.debug(f'Attemping to stitch images in dir: {in_dir}')
    save_dir = '/'.join(save_name.split(os.sep)[:-1])
    create_save_dir_if_needed(save_dir)

    image_files = sorted(glob(in_dir + '/*JPG'))
    images = [cv2.imread(image_file) for image_file in image_files]

    try:
        stitched = stitch_images(images)

        # save and log if it worked
        if stitched is not None:
            cv2.imwrite(f'{save_name}.JPG', stitched)
        else:
            logger.error(f'Could not stitch batch: {save_name}', exc_info=True)
    except Exception as e:
        logger.error(e, exc_info=True)
