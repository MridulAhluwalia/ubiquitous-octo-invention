#!/usr/bin/env python3
"""
Usage: ./main.py -i path_2_input_image -o output_path -s 20
"""
import argparse
import math
import os
import time

from PIL import Image

# -------------------- Constants --------------------

size_name_tuple = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

# -------------------- Argparse --------------------


def parse_arguments():
    def image_type(input_image):
        "check if input type is an image"

        try:
            Image.open(input_image)
            return input_image
        except:
            raise argparse.ArgumentTypeError(
                f"Image path: {input_image} is not a valid image"
            )

    def path_type(path):
        "check if input type is path"

        if os.path.isdir(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"Output path: {path} is not a valid path")

    def size_type(size_type):
        "check size type of the input image"

        if not size_type:
            return
        size_type = size_type.upper()
        if size_type in size_name_tuple:
            return size_type
        else:
            raise argparse.ArgumentTypeError(
                f"Size type should be one of: B, KB, MB, TB..."
            )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_image",
        type=image_type,
        help="input path of the image",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=path_type,
        help="output path of the image",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--output_size",
        type=int,
        help="output size of the image",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--size_type",
        type=size_type,
        help="size type of the image: bytes, kb, mb",
        default=None,
    )
    return parser.parse_args()


# -------------------- Functions --------------------


def convert_size(size_bytes, size_name):
    "convert byte to required size"

    if size_bytes == 0:
        return "0B"
    if not size_name:
        index = int(math.floor(math.log(size_bytes, 1024)))
    else:
        index = size_name_tuple.index(size_name)
    power = math.pow(1024, index)
    size = round(size_bytes / power, 2)
    return size, size_name_tuple[index]


def updated_image_name(image_name, path):
    "add a timestamp to image name and append it output path"

    image_name, extention = image_name.split(".")[:-1], image_name.split(".")[-1]
    new_image_name = (
        ".".join(image_name) + "_" + str(int(time.time())) + "." + extention
    )
    return os.path.join(path, new_image_name)


def compress_image(parsed_args, image_name, current_size):
    "function to compress image size below input threshold"

    image = Image.open(parsed_args.input_image)
    quality = 99
    temp_image = ".".join(["./temp", image_name.split(".")[-1]])

    while current_size > parsed_args.output_size:
        quality -= 5
        if quality <= 0:
            os.remove(temp_image)
            raise Exception(
                f"Error: File cannot be compressed below this: {current_size} {size_type} size"
            )
        image.save(temp_image, optimize=True, quality=quality)
        image = Image.open(temp_image)

        byte_size = os.stat(temp_image).st_size
        current_size, size_type = convert_size(byte_size, parsed_args.size_type)

    os.remove(temp_image)
    return quality


# -------------------- Main --------------------


def main(parsed_args):
    image = Image.open(parsed_args.input_image)

    byte_size = os.stat(parsed_args.input_image).st_size
    size, size_type = convert_size(byte_size, parsed_args.size_type)
    print(f"Input size: {size} {size_type}")

    image_name = parsed_args.input_image.split(os.path.sep)[-1]
    quality = compress_image(parsed_args, image_name, size)
    print(f"Final quality: {quality}")

    output_image = updated_image_name(image_name, parsed_args.output_path)
    image.save(output_image, optimize=True, quality=quality)

    byte_size = os.stat(output_image).st_size
    size, size_type = convert_size(byte_size, parsed_args.size_type)
    print(f"Output image saved is of size: {size} {size_type}")


# -------------------- Start Here --------------------

if __name__ == "__main__":
    parsed_args = parse_arguments()
    main(parsed_args)
