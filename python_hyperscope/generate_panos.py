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

from python_hyperscope.utils import (prepare_directories_for_stitching_in_rows,
                                     create_save_dir_if_needed,
                                     get_memory_usage)
from python_hyperscope.stitch_algorithms import stitch_images_in_dir

logger = logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default=None, required=True,  help='Input directory of images to stitch')
    parser.add_argument('-s', '--stitch', default=False, type=bool, help='Bool to stitch or not. Only preps if False.')
    args = parser.parse_args()

    time = datetime.now().strftime('%Y%m%d%H%M%S')
    sample = args.input_dir.split(os.sep)[1]
    save_dir_base = f'{sample}_rows_{time}_'

    if not os.path.isdir(args.input_dir):
        logger.warning(f'Directory {args.input_dir} does not exist.')
        sys.exit()

    logger.info('Preparing directory for stitching in rows.')
    prepare_directories_for_stitching_in_rows(input_dir=args.input_dir)

    if args.stitch:
        logger.info('Attempting to stitch images in rows.')
        dir_image_rows = os.path.join(args.input_dir, 'rows')
        create_save_dir_if_needed(dir_image_rows)

        # stitch the images in rows (skip root)
        input_dir_tree_pbar = tqdm(sorted(list(os.walk(args.input_dir)))[1:])
        for i, (input_sub_dir, _, _) in enumerate(input_dir_tree_pbar):
            input_dir_tree_pbar.set_description(f'{get_memory_usage()}MB')

            save_name = os.path.join(dir_image_rows, input_sub_dir.split('/')[-1])
            stitch_images_in_dir(
                in_dir=input_sub_dir,
                save_name=save_name,
             )
        logger.info('Attempting to stitch rows into final image.')

        # stitch the row images to a final giant panoramic
        final_output_dir = os.path.join(args.input_dir, 'output')
        create_save_dir_if_needed(final_output_dir)
        stitch_images_in_dir(
            in_dir=dir_image_rows,
            save_name=final_output_dir,
        )
        logger.info('Stitching of final panoramic completed.')
    logger.info('Pipeline completed!')
