import inspect, sys

"""
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