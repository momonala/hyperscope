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

BORDER_X = 1
BORDER_Y = 1


def stitch_images_in_dir(in_dir, save_name):
    """ Stitch Images in batches, growing at each function call.
    Args:
        in_dir (str): input directory of images to batch and stitch
        save_name (str): output file name for temporary panoramics

    Returns: Nothing. Creates Pano in microscope_images_processed/tmp_panoX/ directories as a side effect.
    """
    logger.info(f'Attemping to stitch images in dir: {in_dir}')
    save_dir = '/'.join(save_name.split(os.sep)[:-1])
    create_save_dir_if_needed(save_dir)

    image_files = sorted(glob(in_dir + '/*'))
    images = [cv2.imread(image_file) for image_file in image_files]

    try:
        stitched = stitch_images(images)

        # save and log if it worked
        if stitched is not None:
            cv2.imwrite(f'{save_name}.JPEG', stitched)
        else:
            logger.error(f'Stitching Error: batch: {in_dir}')
    except Exception as f:
        logger.error(f)


def stitch_image_in_batches(in_dir, save_dir, batch_size, skip=1, crop=False):
    """ Stitch Images in batches, growing at each function call.
    Args:
        in_dir (str): input directory of images to batch and stitch
        save_dir (str): output directory of temporary panoramics
        batch_size (int): size of image batch to merge at each iteration
        skip (int): number of images to skip if they are too close to each other
        crop (bool): whether to crop image edges. See globals for number of pixels.

    Returns: Nothing. Creates Pano in microscope_images_processed/tmp_panoX/ directories as a side effect.
    """
    # prepare
    failures = []
    create_save_dir_if_needed(save_dir)
    rm_files_in_dir(save_dir)

    # glob up images, create batches, remove batches of size 1
    image_files = sorted(glob(in_dir + '/*'))[::skip]
    batch_size = len(image_files) if batch_size > len(image_files) else batch_size

    batches = [image_files[i:i + batch_size]
               for i in range(0, len(image_files), batch_size - 1)]
    batches = [batch for batch in batches if len(batch) != 1]

    # iterate through batches, attempt to stitch, write image.
    for i, batch in enumerate(tqdm(batches)):
        images = [cv2.imread(image_file) for image_file in batch]
        images = [crop_border(img, BORDER_X, BORDER_Y) for img in images] if crop else images

        try:
            stitched = stitch_images(images)

            # save and log if it worked
            if stitched is not None:
                cv2.imwrite(f'{save_dir}{i:04}.JPEG', stitched)
            else:
                logger.error(f'Stitching Error: batch: {batch}')
                failures.append(batch)
        except Exception as f:
            logger.error(f)
            failures.append(batch)

    logger.info(failures)


def stitch_seqentially(in_dir, skip=1):
    """ Stitch images sequentially, meaning merge one image at a time to the panoromaic.
    Args:
        in_dir (str): input directory to glob files from and merge.
        skip (int): number of images to skip if they are too close to each other

    Returns:
        Returns: Nothing. Creates pano .jpeg in microscope_images_processed/sequential/ directory as a side effect.

    """
    # prepare
    image_files = sorted(glob(in_dir + '/*'))[::skip]
    save_dir = 'microscope_images_processed/sequential/'
    rm_files_in_dir(save_dir)
    failures = []

    # iterate through image files, attempt to stitch each new image into the growing pano
    for i, image_file in enumerate(tqdm(image_files)):
        if i == 0:
            img1 = crop_border(cv2.imread(image_file), BORDER_X, BORDER_Y)
            continue
        img2 = crop_border(cv2.imread(image_file), BORDER_X, BORDER_Y)

        stitched = stitch_images([img1, img2])

        if stitched is None:
            failures.append(image_file)
        else:
            img1 = stitched
            cv2.imwrite(f'{save_dir}{i:03}.JPEG', stitched)
