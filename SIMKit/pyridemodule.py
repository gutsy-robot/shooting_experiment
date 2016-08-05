class PyRideModule():
	def __init__(self):
		pass
		
	@staticmethod
	def getInstalledModule():
		pyride_modules = ['PyPR2', 'PyREEM']
		for module in pyride_modules:
			try:
				__import__(module)
				return module
			except ImportError:
				continue
		
		return None

