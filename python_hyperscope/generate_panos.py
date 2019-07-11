"""Script to prepare and process images for stitching.

To run:
    python -m python_hyperscope.generate_panos \
        -i microscope_images/<sample directory>/ \
        -s <bool to stitch or not>
"""

import argparse
import logging
import os
import sys
from datetime import datetime

from tqdm import tqdm

from python_hyperscope.utils import prepare_directories_for_stitching_in_rows
from python_hyperscope.stitch_algorithms import stitch_images_in_dir

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default=None, required=True,
                        help='input directory of images to stitch')
    parser.add_argument('-s', '--stitch', default=False, type=bool,
                        help='Whether to stitch or not. Will just prep if False.')
    args = parser.parse_args()

    logger.info(f'Stitching directory {args.input_dir} in rows.')

    time = datetime.now().strftime('%Y%m%d%H%M%S')
    sample = args.input_dir.split(os.sep)[1]
    save_dir_base = f'{sample}_rows_{time}_'

    if not os.path.isdir(args.input_dir):
        logger.info(f'Directory {args.input_dir} does not exist.')
        sys.exit()

    logger.info('Preparing directory for stitching in rows.')
    prepare_directories_for_stitching_in_rows(input_dir=args.input_dir)

    if args.stitch:
        logger.info('Attempting to stitch images.')
        for i, (input_sub_dir, _, _) in enumerate(tqdm(sorted(list(os.walk(args.input_dir))))):
            if i > 0:
                save_name = input_sub_dir.replace('microscope_images', 'microscope_images_processed')
                stitch_images_in_dir(
                    in_dir=input_sub_dir,
                    save_name=save_name,
                 )
        logger.info('Stitching completed!')
    logger.info('Pipeline completed!')
