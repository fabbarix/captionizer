import glob
import os

from captioner import caption_from_path


def find_images(root_folder, glob_pattern="**/*.*"):
    return list(glob.glob(f'{root_folder}{os.path.sep}{glob_pattern}', recursive=True))

# This is for demo purposed


def find_captions():
    base_path = './sd/data'
    files = find_images(base_path)
    for file in files:
        caption = caption_from_path(file, base_path, 'person', 'randoguy')
        print(f'{file} => "{caption}"')


if __name__ == '__main__':
    find_captions()
