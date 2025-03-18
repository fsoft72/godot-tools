#!/usr/bin/env python3

"""
This script takes a directory of images and creates a spritesheet from them.
The directory can contain different animations, each with a different name prefix.
The script will create a spritesheet for each animation.

Each spritesheet size is determined by the largest image in the animation.
The script will pad smaller images with transparency to match the size of the largest image, centered.
"""

import os
import sys
import argparse
import PIL.Image


def get_args():
    parser = argparse.ArgumentParser(
        description="Create spritesheets from a directory of images."
    )
    parser.add_argument(
        "input_dir", help="Directory containing images to be converted to spritesheets."
    )
    parser.add_argument("output_dir", help="Directory to save the spritesheets to.")
    parser.add_argument(
        "--format", default="png", help="Format of the spritesheet (png, jpg, etc)."
    )
    return parser.parse_args()


def get_animations(input_dir):
    """
    Scan the input directory for images and group them into animations.
    An animation is a sequence of images with the same prefix.
    The images must be named with the format 'prefix_frame.ext'.
    """
    animations = {}
    for filename in os.listdir(input_dir):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in (".png", ".jpg", ".jpeg", ".gif"):
            continue
        if "_" in name:
            name, frame = name.rsplit("_", 1)
            if not frame.isdigit():
                continue
        else:
            frame = 0
        frame = int(frame)
        if name not in animations:
            animations[name] = []
        animations[name].append(filename)
    return animations


def create_spritesheet(animation, input_dir, output_dir, format):
    frames = sorted(animation)
    filenames = [os.path.join(input_dir, frame) for frame in frames]
    images = [PIL.Image.open(filename) for filename in filenames]
    width, height = max(image.size for image in images)

    spritesheet = PIL.Image.new("RGBA", (width * len(images), height))
    for i, image in enumerate(images):
        x = i * width + (width - image.width) // 2
        y = (height - image.height) // 2
        spritesheet.paste(image, (x, y))

    name = animation[0].rsplit("_", 1)[0]
    output_filename = os.path.join(output_dir, f"{name}.{format}")
    spritesheet.save(output_filename, format=format)
    print(f"Saved {output_filename}")


def main():
    args = get_args()
    animations = get_animations(args.input_dir)
    for animation in animations.values():
        create_spritesheet(animation, args.input_dir, args.output_dir, args.format)


if __name__ == "__main__":
    main()
