# Captions from filenames

This module creates captions from images in a folder based on
the folder names and the name of the image file.

```python
>>> from captioner import caption_from_path

```

In the following examples we assume that:

 - Token is 'randoguy'
 - Class for the token is 'person'
 - The base of our test data is `/sd/data`

```py
>>> class_token = 'person'
>>> token = 'randoguy'
>>> base_path = '/sd/data'

```

In the simplest case - if a file is in the root of the folder -
it will behave the same way as it does today. So:

```py
>>> print(caption_from_path('/sd/data/img-001.jpg', base_path, class_token, token))
randoguy person

```

Next up - if you have an image file in `/sd/data/joepenna/img-001.jpg` your *token*, if
passed, will be ignored and *joepenna* is going to be used to create the caption.

```py
>>> print(caption_from_path('/sd/data/joepenna/img-001.jpg', base_path, class_token, token))
joepenna person

```
One deeper: if you have an image file in `/sd/data/joepenna/person/img-001.jpg` things get
more interesting: the first part is used as a token the second as a class, so you get:

```py
>>> print(caption_from_path('/sd/data/joepenna/man/img-001.jpg', base_path, class_token, token))
joepenna man

```
This allows you to train the same subject under different classes (*man*, *person*, *biped*)

Finally: you can customize the caption by adding an annotation to the filename, so:
`/sd/data/joepenna/person/img-001@a_picture_of_S.jpg` would look like:

```py
>>> print(caption_from_path('/sd/data/joepenna/person/img-001@a_picture_of_S.jpg', base_path, class_token, token))
a picture of joepenna

```

You can see that '*S*' was automatically converted to the subject token. I can hear you scream: 'But what if I
want to have an "S" in my caption?' - well: *tough luck*! And wait until I tell you that I also eating all your
*T*s! Yes: if you have a file in `/sd/data/joepenna/dude/img-001@S_the_C_hanging_out_by_the_pool.jpg` then
your caption becomes:

```py
>>> filename = '/sd/data/joepenna/dude/img-001@S_the_C_hanging_out_by_the_pool.jpg'
>>> print(caption_from_path(filename, base_path, class_token, token))
joepenna the dude hanging out by the pool

```

But wait! There is more!

If you don't want to caption all of your images -- who has the time anyhow, right? -- you can have
something along these lines: `/sd/data/joepenna/dude/a_picture_of_S_being_a_C/img-001@as_a_C_can_be.jpg` to get:

```py
>>> filename = '/sd/data/joepenna/dude/a_picture_of_S_being_a_C/img-001@as_a_C_can_be.jpg'
>>> print(caption_from_path(filename, base_path, class_token, token))
a picture of joepenna being a dude as a dude can be

```

Finally - I promise - you can use captions directly in the old fashioned *let's dump all of our
images in the same bucket* method, so `/sd/data/img-001@S_being_a_handsome_C.jpg` would spit out:

```py
>>> filename = '/sd/data/img-001@S_being_a_handsome_C.jpg'
>>> print(caption_from_path(filename, base_path, class_token, token))
randoguy being a handsome person

```

## The finder

Now that we have a more complex structure you can see that listing the files in a folder is no
longer enough, we need to be able to recursively find them given a root data folder. Lucky us:

```py
from finder import find_images

print(find_images('/sd/data'))
```

If you want to see what all of this sums up to, you can run:

```bash
python3 finder.py
```

## Running this document as a python test

You what? Really? You don't trust me?? OK:

```bash
python3 run_tests.py
```

