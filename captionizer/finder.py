import glob
import os
import sys

from .captionizer import caption_from_path


def find_images(root_folder, glob_pattern="**/*.*"):
    return list(glob.glob(f'{root_folder}{os.path.sep}{glob_pattern}', recursive=True))


def find_captions(base_path='./sd/data'):
    files = find_images(base_path)
    for file in files:
        caption = caption_from_path(file, base_path, 'person', 'randoguy')
        print(f'{file} => "{caption}"')


def main():
    base_path = '.'
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    find_captions(base_path)


if __name__ == '__main__':
    main()
