from jaratoolbox import loadbehavior as lr
from jaratoolbox import behavioranalysis as ba
import numpy as np
class ArraData:
	
	array = np.array([])
	data = None
	
	#init the class
	def __init__(self,Data):
		#get the behavior data from here
		self.data = Data
	
	#main function, return an particular array to the plot builder
	def get_array(self,plot_type):
		#analyze the data and slice the info to build a psychometric graph
		if plot_type == 'psychometric':
			print "return psychometric array"
			print self.data['choice']
			return self.data['choice']
		#analyze the data and slice the info to build a summary graph
		elif plot_type == 'summary':
			print self.data['nValid'][-1]
			print "return summary array"
			return self.data['nValid'][-1]
		#analyze the data and slice the info to build a dynamics graph
		elif plot_type == 'dynamics':
			print self.data.labels['choice']['left']
			print "return dynamics array"
		# type not found
			return self.data.labels['choice']['left']
		else:
			print "no this type of plot"
			array = None
		return self.array
