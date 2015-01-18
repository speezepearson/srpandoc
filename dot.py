#!/Users/spencerpearson/.virtualenv/python3.4.1/bin/python

import subprocess
from .figures import figure_replacer


def make_graph(block, filename, extension):
    p = subprocess.Popen(['dot', '-T'+extension, '-o'+filename], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    input = "graph _{"+block.content+"}"
    (out, err) = p.communicate(input.encode())
    if p.returncode != 0:
        raise RuntimeError('DOT error: {}'.format(err.decode()))

graph_filter = figure_replacer("dot", make_graph)
