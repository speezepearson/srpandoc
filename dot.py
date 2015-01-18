import subprocess
from .figures import figure_replacer


def make_graph(block, filename, extension):
    """Draws a graph using DOT.
    """
    p = subprocess.Popen(['dot', '-T'+extension, '-o'+filename], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    graph_type = "digraph" if "directed" in block.classes else "graph"
    input = graph_type + " _{"+block.content+"}"
    (out, err) = p.communicate(input.encode())
    if p.returncode != 0:
        raise RuntimeError('DOT error: {}'.format(err.decode()))

graph_filter = figure_replacer("dot", make_graph)
