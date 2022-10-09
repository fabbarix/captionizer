import os
import re
from typing import OrderedDict


splitter = re.compile(r'\s|_')


def has_caption(filename):
    if filename is None:
        return False
    return '@' in filename or os.path.dirname(filename) != ''


def contains_tokens(template):
    parts = splitter.split(template)
    return 'S' in parts or 'C' in parts


def fill_template(template, tokens):
    parts = [
        tokens[part] if part in tokens.keys()
        else part
        for part in splitter.split(template)
    ]
    return ' '.join(parts)


def template_from_path(filepath, tokens):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    filetpl = ''
    pathtpl = ' '.join(os.path.dirname(filepath).split(os.path.sep))
    filetpl = ' '.join(tokens.keys())

    if '@' in filename:
        filetpl = filename.split('@')[1]
    elif contains_tokens(pathtpl):
        filetpl = ''

    separator = ' ' if pathtpl and filetpl else ''
    return f'{pathtpl}{separator}{filetpl}'


def filename_caption(tokens, filepath):
    filename_tpl = template_from_path(filepath, tokens)
    caption = fill_template(filename_tpl, tokens)
    return caption


def token_caption(tokens, filename=None):
    if has_caption(filename):
        caption = filename_caption(tokens, filename)
    else:
        caption = ' '.join([tokens[key] if tokens[key] else '' for key in tokens.keys()])
    return caption


def path_caption(rel_path, tokens):
    image_path = os.path.dirname(rel_path).split(os.path.sep)
    if len(image_path) == 0:
        caption = token_caption(tokens)
    else:
        token_keys = list(tokens.keys())
        max_replacements = min(len(token_keys), len(image_path))
        for key_idx in range(max_replacements):
            tokens[token_keys[key_idx]] = image_path[key_idx]
        new_path = os.path.relpath(
            rel_path, os.path.sep.join(image_path[:max_replacements]))
        caption = token_caption(tokens, new_path)
    return caption


def generic_captions_from_path(file_path, base_path, tokens):
    rel_path = os.path.relpath(file_path, base_path)
    parent_path = os.path.dirname(rel_path)
    caption = 'broken caption'
    if parent_path == '':
        caption = token_caption(tokens, rel_path)
    else:
        caption = path_caption(rel_path, tokens)
    return caption


def caption_from_path(file_path, base_path, class_token=None, token=None):
    # Prefer OrderedDict - key order in regular dict is only guaranteed
    # from Python 3.7 onward.
    tokens = OrderedDict([('S', token), ('C', class_token)])
    return generic_captions_from_path(file_path, base_path, tokens)
