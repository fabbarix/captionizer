import os
import re

splitter = re.compile(r'\s|_')

def has_caption(filename):
    if filename is None:
        return False
    return '@' in filename or os.path.dirname(filename) != ''


def contains_tokens(template):
    parts = splitter.split(template)
    return 'S' in parts or 'C' in parts


def fill_template(template, token, class_token):
    parts = [token if part == 'S' else part for part in splitter.split(template)]
    parts = [class_token if part == 'C' else part for part in parts]
    return ' '.join(parts)


def template_from_path(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    filetpl = ''
    pathtpl = ' '.join(os.path.dirname(filepath).split(os.path.sep))
    filetpl = 'S C'

    if '@' in filename:
        filetpl = filename.split('@')[1]
    elif contains_tokens(pathtpl):
        filetpl = ''

    separator = ' ' if pathtpl and filetpl else ''
    return f'{pathtpl}{separator}{filetpl}'


def filename_caption(token, class_token, filepath):
    caption = fill_template(template_from_path(filepath), token, class_token)
    return caption


def token_caption(token, class_token, filename=None):
    if has_caption(filename):
        caption = filename_caption(token, class_token, filename)
    else:
        caption = f'{token} {class_token}' if class_token else f'{token}'
    return caption


def path_caption(rel_path, class_token, token):
    image_path = os.path.dirname(rel_path).split(os.path.sep)
    caption = token_caption(token, class_token)
    if len(image_path) == 1:
        caption = token_caption(
            image_path[0],
            class_token,
            os.path.relpath(rel_path, image_path[0])
        )
    else:
        caption = token_caption(
            image_path[0],
            image_path[1],
            os.path.relpath(rel_path, os.path.join(
                image_path[0], image_path[1]
            )),
        )
    return caption


def caption_from_path(file_path, base_path, class_token=None, token=None):
    rel_path = os.path.relpath(file_path, base_path)
    parent_path = os.path.dirname(rel_path)
    caption = 'broken caption'
    if parent_path == '':
        caption = token_caption(token, class_token, rel_path)
    else:
        caption = path_caption(rel_path, class_token, token)
    return caption
