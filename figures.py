import hashlib
import os
import pandocfilters

from .blocks import CodeBlock

def preferred_basefilename(block):
    return block.attrs.get("basefilename")

def filename(block):
    hash = hashlib.sha256(block.content.encode('utf-8')).hexdigest()
    preferred_base = preferred_basefilename(block)
    ext = extension(block)

    segments = [preferred_base] if preferred_base else []
    segments.append(hash)
    if ext:
        segments.append(ext)

    return ".".join(segments)

def extension(block, default="png"):
    if "format" in block.attrs:
        return block.attrs["format"]
    elif preferred_basefilename(block) and "." in preferred_basefilename(block):
        return preferred_basefilename(block).rsplit(".", 1)[-1]
    return default

def figure_replacer(cls, make_image):
    def replace(block):
        if not ("figure" in block.classes and cls in block.classes):
            return None
        if not os.path.exists(filename(block)):
            make_image(block, filename(block), extension(block))
        return image_pandocblock(filename=filename(block), alt_text=block.content)
    return replace

def image_pandocblock(filename, alt_text):
    return pandocfilters.Para([pandocfilters.Image([], [filename, alt_text])])

def avoids_recreation(f):
    def lazy_f(block):
        if os.exists(filename(block)):
            return None
        return f(block)
    return lazy_f