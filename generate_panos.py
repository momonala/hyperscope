import argparse
import logging
from glob import glob

import cv2
from tqdm import tqdm
from utils import crop_border, rm_files_in_dir

STOP = -1

logger = logging.getLogger(__name__)


def stitch_image_in_batches(in_dir, out_dir, batch_size, crop=False):
    """ Stitch Images in batches, growing at each function call.
    Args:
        in_dir (str): input directory of images to batch and stitch
        out_dir (str): output directory of temporary panoramics
        batch_size (int): size of image batch to merge at each iteration
        crop (bool): whether to crop image edges. See globals for number of pixels.

    Returns: Nothing. Creates Pano in tmp/tmp_panoX/ directories as a side effect.
    """
    BORDER_X = 1
    BORDER_Y = 1

    # prepare
    rm_files_in_dir(out_dir)
    failures = []

    # glob up images, create batches, remove batches of size 1
    image_files = sorted(glob(in_dir + '/*'))
    batches = [image_files[i:i + batch_size]
               for i in range(0, len(image_files), batch_size - 1)][:STOP]
    batches = [batch for batch in batches if len(batch) != 1]

    # iterate through batches, attempt to stitch, write image.
    for batch in tqdm(batches):
        images = [cv2.imread(image_file) for image_file in batch]
        images = [crop_border(img, BORDER_X, BORDER_Y) for img in images] if crop else images

        try:
            stitcher = cv2.createStitcher()
            status, stitched = stitcher.stitch(images)

            # save and log
            if status == 0:
                cv2.imwrite(f'{out_dir}{i:04}.JPEG', stitched)
            else:
                failures.append(f'Stitching Error: batch: {batch}')
        except:
            failures.append(f'OpenCV System Error: batch: {batch}')

    logger.info(failures)


def stitch_seqentially(in_dir):
    """ Stitch images sequentially, meaning merge one image at a time to the panoromaic.
    Args:
        in_dir (str): input directory to glob files from and merge.
    Returns:
        np.ndarray: very large, and hopefully beautiful pano

    """
    image_files = sorted(glob(in_dir + '/*'))

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default=None)
    parser.add_argument('-s', '--stitching_algo', default=None)
    args = parser.parse_args()

    if args.stitching_algo == 'batches':
        tmp_panos0 = 'tmp/tmp_panos0/'
        stitch_image_in_batches(args.input_dir, tmp_panos0, batch_size=2, crop=False)
        for i in range(7):
            stitch_image_in_batches(f'tmp/tmp_panos{i}/',
                                    f'tmp/tmp_panos{i+1}/',
                                    batch_size=i + 2)

    elif args.stitching_algo == 'sequential':
        stitch_seqentially(args.input_dir)


