"""Script to prepare and process images for stitching.

To run:
    python -m python_hyperscope.generate_panos \
        --input_dir microscope_images/<sample directory>/ \
        --prepare <bool to prepare directories or not>
"""

import argparse
import logging
import os
import subprocess
import sys
from time import time

from tqdm import tqdm

from python_hyperscope.stitch_algorithms import stitch_images_from_list
from python_hyperscope.utils import (
    prepare_directories_for_stitching_in_rows,
    get_memory_usage,
    sort_jpg_files_in_dir_alpha,
    format_directories,
)

logger = logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

OVERLAP = 6  # number of images in chunk that overlap
SKIP = False  # only every other image
DEBUG = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_dir",
        default=None,
        required=True,
        type=str,
        help="Input directory of images to stitch.",
    )
    parser.add_argument(
        "-p",
        "--prepare",
        default=True,
        required=False,
        type=lambda x: (str(x).lower() == "true"),
        help="Whether to prepare directories or not (bool).",
    )
    parser.add_argument(
        "-c",
        "--chunk_size",
        default=10,
        required=True,
        type=int,
        help="size of sub list of images in row to process (set to 100 to process whole row.)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        logger.warning(f"Directory {args.input_dir} does not exist.")
        sys.exit()

    t0 = time()
    logger.info("Preparing directory for stitching in rows.")
    if args.prepare:
        prepare_directories_for_stitching_in_rows(input_dir=args.input_dir)
    (
        dir_image_rows,
        dir_final_output,
        path_final_output,
        dir_dzi,
        path_dzi,
    ) = format_directories(args.input_dir)

    # get all image dirs and stitch the rows
    logger.info("Attempting to stitch images in rows.")
    logger.info(
        f"Chunk size: {args.chunk_size} \tOverlap: {OVERLAP} \tSkipping: {SKIP}"
    )
    input_dir_tree_pbar = tqdm(
        sorted([x[0] for x in os.walk(args.input_dir) if "row" in x[0]])[:-1]
    )

    for i, input_sub_dir in enumerate(input_dir_tree_pbar):
        img_file_list = sort_jpg_files_in_dir_alpha(input_sub_dir)
        img_file_list = img_file_list[::2] if SKIP else img_file_list
        input_dir_tree_pbar.set_description(
            f"batch size: {len(img_file_list)} | memory: {get_memory_usage()} mb"
        )

        # now go through a single row, break into chunks, stitch, then stitch the chunks together
        img_file_list_as_chunks = [
            img_file_list[i : i + args.chunk_size]
            for i in range(0, len(img_file_list), args.chunk_size - OVERLAP)
        ]
        img_file_list_chunks_pbar = tqdm(img_file_list_as_chunks)
        stitched_images_in_chunk = []
        for j, img_file_list_chunk in enumerate(img_file_list_chunks_pbar):
            img_file_list_chunks_pbar.set_description(
                f'Processing chunk {input_sub_dir.split("/")[-1]}-{j}'
            )
            save_path = os.path.join(
                dir_image_rows, f'{input_sub_dir.split("/")[-1]}_{j}'
            )
            stitched_images_in_chunk.append(
                stitch_images_from_list(
                    src_list=img_file_list_chunk,
                    input_type="file",
                    save_name=save_path,
                    save=DEBUG,
                )
            )
        img_file_list_chunks_pbar.set_description(
            f"Stitching full row: {input_sub_dir}"
        )
        stitch_images_from_list(
            src_list=stitched_images_in_chunk,
            save_name=os.path.join(dir_image_rows, f'{input_sub_dir.split("/")[-1]}'),
            input_type="array",
            save=True,
        )

    # stitch the row images to a final giant panoramic
    logger.info("Attempting to stitch rows into final image.")
    stitch_images_from_list(
        src_list=sort_jpg_files_in_dir_alpha(dir_image_rows),
        save_name=path_final_output,
        input_type="file",
        save=True,
    )

    # slice into .dzi
    logger.info(f"Slicing final output into .dzi format. Saving to: {path_dzi}_files")
    slicer_process_status = subprocess.run(
        ["./magick-slicer.sh", f"{path_final_output}.JPG", "-o", f"{path_dzi}"]
    )
    if slicer_process_status.returncode == 1:
        logger.error("Error with slicing.")
        sys.exit()
    logger.info(
        f"Pipeline completed! Processed {len(input_dir_tree_pbar)} images in {round(time()-t0, 2)} sec."
    )
