#!/Users/spencerpearson/.virtualenv/python3.4.1/bin/python

import hashlib

class CodeBlock:
    def __init__(self, content, ident=None, classes=set(), attrs={}, format=None, meta=None):
        self.ident = ident
        self.classes = classes
        self.attrs = attrs
        self.content = content
        self.format = format
        self.meta = meta

    @classmethod
    def from_json(cls, key, value, format, meta):
        if key != "CodeBlock":
            raise ValueError()

        (ident, classes, attrs), content = value
        return cls(ident=ident, classes=set(classes), attrs=dict(attrs), content=content, format=format, meta=meta)

    def to_json(self):
        return pandocfilters.CodeBlock((self.ident, self.classes, self.attrs), self.content)

def json_to_blocks(block_filter):
    def json_function(key, value, format, meta):
        try:
            block = CodeBlock.from_json(key, value, format, meta)
        except ValueError:
            return None
        return block_filter(block)

    return json_function

def run_block_filter(filter):
    pandocfilters.toJSONFilter(json_to_blocks(filter))