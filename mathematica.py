#!/Users/spencerpearson/.virtualenv/python3.4.1/bin/python

import subprocess
from .figures import figure_replacer


def make_mathematica_image(block, filename, extension):
    p = subprocess.Popen(['/Applications/Mathematica.app/Contents/MacOS/MathKernel'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    input = "\n".join((block.content, 'Export["{}", %]'.format(filename)))
    (out, err) = p.communicate(input.encode())
    if p.returncode != 0:
        raise RuntimeError('Mathematica error: {}'.format(err.decode()))

mathematica_filter = figure_replacer("mathematica", make_mathematica_image)
