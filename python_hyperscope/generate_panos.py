import argparse
import logging
import os
import sys
from datetime import datetime

from tqdm import tqdm

from python_hyperscope.stitch_algorithms import stitch_image_in_batches, stitch_seqentially, stitch_images_in_dir

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default=None, help='input directory of images to stitch')
    parser.add_argument('-a', '--stitching_algo', default=None,
                        help='stitching algorithm: `batches`, `dir` or `sequential`')
    parser.add_argument('-b', '--batch_size', default=10, type=int, help='batch size')
    parser.add_argument('-s', '--skip', default=1, type=int, help='interval to skip images')
    args = parser.parse_args()

    if args.stitching_algo not in ['batches', 'sequential', 'dir']:
        logger.error(f'Stitching algorithm must be `batches`, `dir` or `sequential`')
        sys.exit(1)

    time = datetime.now().strftime('%Y%m%d%H%M%S')
    sample = args.input_dir.split(os.sep)[1]
    save_dir_base = f'{sample}_{args.stitching_algo}_{time}_'

    if args.stitching_algo == 'dir':
        for i, (input_sub_dir, _, _) in enumerate(tqdm(sorted(list(os.walk(args.input_dir))))):
            if i > 0:
                save_name = input_sub_dir.replace('microscope_images', 'microscope_images_processed')
                stitch_images_in_dir(
                    in_dir=input_sub_dir,
                    save_name=save_name,

                 )

    elif args.stitching_algo == 'batches':
        stitch_image_in_batches(
            in_dir=args.input_dir,
            save_dir=f'microscope_images_processed/{save_dir_base}panos0/',
            batch_size=args.batch_size,
            skip=args.skip,
            crop=False
        )
        for j in range(7):
            stitch_image_in_batches(
                in_dir=f'microscope_images_processed/{save_dir_base}panos{j}/',
                save_dir=f'microscope_images_processed/{save_dir_base}panos{j+1}/',
                batch_size=args.batch_size,
                skip=1,
                crop=False
            )

    elif args.stitching_algo == 'sequential':
        stitch_seqentially(args.input_dir, skip=args.skip)

