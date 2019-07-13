"""Script to prepare and process images for stitching.

To run:
    python -m python_hyperscope.generate_panos \
        -i microscope_images/<sample directory>/ \
"""

import argparse
import logging
import os
import subprocess
import sys
from time import time

from tqdm import tqdm

from python_hyperscope.stitch_algorithms import stitch_images_in_dir
from python_hyperscope.utils import (prepare_directories_for_stitching_in_rows,
                                     create_save_dir_if_needed,
                                     get_memory_usage)

logger = logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default=None, required=True, help='Input directory of images to stitch')
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        logger.warning(f'Directory {args.input_dir} does not exist.')
        sys.exit()

    t0 = time()
    logger.info('Preparing directory for stitching in rows.')
    prepare_directories_for_stitching_in_rows(input_dir=args.input_dir)

    # pre-format directories and paths
    sample_name = args.input_dir.split(os.sep)[1]
    dir_image_rows = os.path.join(args.input_dir, 'rows')

    dir_final_output = os.path.join(args.input_dir, 'output')
    path_final_output = os.path.join(dir_final_output, 'output')

    dir_dzi = os.path.join(dir_final_output, "dzi")
    path_dzi = os.path.join(dir_dzi, sample_name)

    create_save_dir_if_needed(dir_image_rows)
    create_save_dir_if_needed(dir_final_output)
    create_save_dir_if_needed(dir_dzi)

    # stitch the images in rows
    logger.info('Attempting to stitch images in rows.')
    input_dir_tree_pbar = tqdm(sorted(
        [x[0] for x in os.walk(args.input_dir) if 'row' in x[0]]
    )[1:])
    for i, input_sub_dir in enumerate(input_dir_tree_pbar):
        input_dir_tree_pbar.set_description(f'{get_memory_usage()}MB')

        save_path = os.path.join(dir_image_rows, input_sub_dir.split('/')[-1])
        stitch_images_in_dir(
            in_dir=input_sub_dir,
            save_name=save_path,
         )

    # stitch the row images to a final giant panoramic
    logger.info('Attempting to stitch rows into final image.')
    stitch_images_in_dir(
        in_dir=dir_image_rows,
        save_name=path_final_output,
    )

    # slice into .dzi
    logger.info(f'Slicing final output into .dzi format. Saving to: {path_dzi}_files')
    slicer_process_status = subprocess.run([
        './magick-slicer.sh',
        f'{path_final_output}.JPG',
        '-o',
        f'{path_dzi}'
    ])
    if slicer_process_status.returncode == 1:
        logger.error('Error with slicing.')
        sys.exit()
    logger.info(f'Pipeline completed! Processed {len(input_dir_tree_pbar)} images in {round(time()-t0, 2)} sec.')
