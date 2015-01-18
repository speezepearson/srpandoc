#!/Users/spencerpearson/.virtualenv/python3.4.1/bin/python

import pylab
from .blocks import json_to_blocks
from .figures import figure_replacer

def make_plot(block, filename, extension):
    exec(block.content, pylab.__dict__, {})
    pylab.savefig(filename)

plot_filter = figure_replacer("plot", make_plot)
