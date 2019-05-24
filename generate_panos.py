import argparse
import logging
import os
import sys
from datetime import datetime

from stitch_algorithms import stitch_image_in_batches, stitch_seqentially

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', default=None, help='input directory of images to stitch')
    parser.add_argument('-a', '--stitching_algo', default=None, help='stitching algorithm: `batches` or `sequential`')
    parser.add_argument('-b', '--batch_size', default=10, type=int, help='batch size')
    parser.add_argument('-s', '--skip', default=1, type=int, help='interval to skip images')
    args = parser.parse_args()

    if args.stitching_algo not in ['batches', 'sequential']:
        logger.error(f'Stitching algorithm must be `batches` or `sequential`')
        sys.exit(1)

    time = datetime.now().strftime('%Y%m%d%H%M%S')
    sample = args.input_dir.split(os.sep)[1]
    save_dir_base = f'{sample}_{args.stitching_algo}_{time}_'

    if args.stitching_algo == 'batches':
        stitch_image_in_batches(
            in_dir=args.input_dir,
            save_dir=f'tmp/{save_dir_base}panos0/',
            batch_size=args.batch_size,
            skip=args.skip,
            crop=False
        )
        for j in range(7):
            stitch_image_in_batches(
                in_dir=f'tmp/{save_dir_base}panos{j}/',
                save_dir=f'tmp/{save_dir_base}panos{j+1}/',
                batch_size=args.batch_size,
                skip=1,
                crop=False
            )

    elif args.stitching_algo == 'sequential':
        stitch_seqentially(args.input_dir)


