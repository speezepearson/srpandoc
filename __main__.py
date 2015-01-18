from pandocfilters import toJSONFilter
from srpandoc import union_filter
from srpandoc.blocks import json_to_blocks
from srpandoc.plot import plot_filter
from srpandoc.dot import graph_filter
from srpandoc.mathematica import mathematica_filter

FILTERS = (plot_filter, graph_filter, mathematica_filter)

toJSONFilter(json_to_blocks(union_filter(*FILTERS)))