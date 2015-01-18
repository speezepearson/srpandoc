"""Acts as a Pandoc JSON filter to replace some kinds of code block with resources.
"""

import pandocfilters
from srpandoc import union_filter
from srpandoc.blocks import json_to_blocks
from srpandoc.plot import plot_filter
from srpandoc.dot import graph_filter
from srpandoc.mathematica import mathematica_filter

FILTERS = (plot_filter, graph_filter, mathematica_filter)

total_filter = union_filter(*FILTERS)
def safe_total_filter(block):
  """Tries to apply any `FILTER` to the given block and return the result; if there's an error, return a boring 'there was an error' block.
  """
  try:
    return total_filter(block)
  except (RuntimeError, FileNotFoundError) as e:
    return pandocfilters.Para([pandocfilters.Str("(Error generating image: {})".format(e))])

pandocfilters.toJSONFilter(json_to_blocks(safe_total_filter))