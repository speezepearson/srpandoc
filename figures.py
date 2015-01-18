import hashlib
import os
import pandocfilters

from .blocks import CodeBlock

def preferred_basefilename(block):
    """Tries to guess a good, descriptive base filename for a block's image.
    """
    return block.attrs.get("basefilename")

def extension(block, default="png"):
    """Tries to guess the file extension for the block's image.
    """
    if "format" in block.attrs:
        return block.attrs["format"]
    elif preferred_basefilename(block) and "." in preferred_basefilename(block):
        return preferred_basefilename(block).rsplit(".", 1)[-1]
    return default

def filename(block):
    """Returns the filename that should be given to a block's image.

    The filename will start with the block's resource's desired filename (if any), and end with the block's desired extension (if determinable), and will contain a checksum of the block's content.
    """
    hash = hashlib.sha256(block.content.encode('utf-8')).hexdigest()
    preferred_base = preferred_basefilename(block)
    ext = extension(block)

    return "{base}{hash}{ext}".format(
        base=(preferred_base+".") if preferred_base else "",
        hash=hash,
        ext=("."+ext) if ext else ""
    )

def figure_replacer(cls, make_image):
    """Returns a function that tries to transform code blocks into images.

    Arguments:

    - `cls` (string):
      the class that a block must have (in addition to "figure") to be replaceable
    - `make_image` (function: block, filename (string), extension (string) -> None):
      given a block, filename, and file extension, create the image described by the block and save it as that file.

    Returns either:
    - a Pandoc block containing the image created by `make_image`, if the block has the appropriate classes; or
    - None, otherwise.
    """
    def replace(block):
        if not ("figure" in block.classes and cls in block.classes):
            return None
        f = filename(block)
        if not os.path.exists(f):
            make_image(block, f, extension(block))
        return image_pandocblock(filename=f, alt_text=block.content)
    return replace

def image_pandocblock(filename, alt_text):
    """Return a Pandoc block that has an Image in it.
    """
    return pandocfilters.Para([pandocfilters.Image([], [filename, alt_text])])
