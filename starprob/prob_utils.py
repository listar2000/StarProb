import inspect, sys

"""
Effective way of raising undefined value is inspired by Berkeley AI project
@source https://inst.eecs.berkeley.edu/~cs188/fa19/project3/
"""
def raiseUndefined():
    frame = inspect.stack()[1]
    fileName, line, method = frame[1], frame[2], frame[3]
    print("*** Method not implemented: %s at line %s of %s" %
          (method, line, fileName))
    sys.exit(1)

def raiseMissingArgument(argname):
	frame = inspect.stack()[1]
	fileName, method = frame[1], frame[3]
	print("*** Argument %s missing from method %s in %s" % 
		  (argname, method, fileName))
	sys.exit(1)

class raiseIllValue(Exception):
	def __init__(self, condition, show_class = False):
		frame = inspect.stack()[1]
		line, method = frame[2], frame[3]
		original_cb = sys.excepthook
		def error_callback(a, b, c):
			if show_class:
				calling_class = frame[0].f_locals["self"].__class__
				print("*** Value Error: %s at line %s in %s() at %s" % 
				(condition, line, method, calling_class))
			else:
				print("*** Value Error: %s at line %s in method %s" % 
				(condition, line, method))
			# return original call_back after using this custom exception
			sys.excepthook = original_cb
		sys.excepthook = error_callback

def raiseIfNotAllNumeric(*collections):
	for collection in collections:
		flag = all([isinstance(i, (int, float)) for i in collection])
		if not flag:
			varName, method = None, None
			for fi in reversed(inspect.stack()):
				for k, v in fi.frame.f_locals.items():
					if v is collection:
						varName = k
						method = fi[3]
						print("*** Elements of %s in method %s should be all numeric" %
							(varName, method))
						sys.exit(1)