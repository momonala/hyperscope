"""Panoramic Stitching Algorithms."""

import logging
import os
import cv2
from functools import partial
from python_hyperscope.utils import crop_border, stitch_images, create_dir_if_needed

logger = logging.getLogger(__name__)


def stitch_images_from_list(src_list, save_name, input_type, crop=True, save=True):
    """Stitch Images in batches, growing at each function call.

    Args:
        src_list (list): list of images to stitch
        save_name (str): output file name for temporary panoramics
        input_type (str): one of [array, file] - img source is np.array or image file.
        crop (bool): whether to crop or not
        save (bool): whether to save or not

    Returns: Nothing. Creates Pano in microscope_images_processed/tmp_panoX/ directories as a side effect.
    """
    logger.debug(f"Attemping to stitch images in dir: {save_name}")
    if input_type == "file":
        crop_border_fn = (
            partial(crop_border, border_x=200, border_y=200) if crop else lambda x: x
        )
        images = [crop_border_fn(cv2.imread(image_file)) for image_file in src_list]
    elif input_type == "array":
        images = src_list

    try:
        stitched_image = stitch_images(images)

        # save and log if it worked
        if stitched_image is not None:
            if save:
                save_dir = "/".join(save_name.split(os.sep)[:-1])
                create_dir_if_needed(save_dir)
                cv2.imwrite(f"{save_name}.JPG", stitched_image)
            return stitched_image
        else:
            logger.error(f"Could not stitch batch: {save_name}", exc_info=True)
    except Exception as e:
        logger.error(e, exc_info=True)
