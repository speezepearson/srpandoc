from . import blocks, dot, figures, plot, mathematica

def union_filter(*filters):
	filters = tuple(filters)
	def union(*args, **kwargs):
		for filter in filters:
			result = filter(*args, **kwargs)
			if result is not None:
				return result
		return None
	return union
