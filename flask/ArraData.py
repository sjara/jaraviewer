import loadbehavior as lr
import behavioranalysis as ba
import numpy as np
class ArraData:

	array = []
	data = 1
	dict = {}
	name = ""
	session = ""
	paradigm = ""
	#init the class
	def __init__(self,Data):
		#get the behavior data from here
		self.data = Data
		
		
	
	#main function, return an particular array to the plot builder
	def arrange_data(self,plot_type):
		self.dict['name'] = self.name
		self.dict['choice'] = self.data['choice']
		self.dict['session'] = self.session
		self.dict['paradigm'] = self.paradigm
		#analyze the data and slice the info to build a psychometric graph
		if plot_type == 'psychometric':
			print "arrange psychometric data"
			self.dict['plot_type'] = 'psychometric'
			self.array.append(self.dict)
			return "arrange success"
		#analyze the data and slice the info to build a summary graph
		elif plot_type == 'summary':
			print "arrange summary data"
			self.dict['plot_type'] = 'summary'
			self.array.append(self.dict)
			return "arrange success"
		#analyze the data and slice the info to build a dynamics graph
		elif plot_type == 'dynamics':
			print "arrange dynamics data"
			self.dict['plot_type'] = 'dynamics'
			self.array.append(self.dict)
			return "arrange success"
		# type not found
		else:
			print "no this type of plot"
			return "arrange failed"
		

	def get_array(self):
		temp = self.array
		self.clean()
		return temp	
	
	def switch_data(self,data):
		self.data = data

	def get_Data(self):
		return self.data

	def set_name(self,name):
		self.name = name

	def set_session(self,session):
		self.session = session

	def set_paradigm(self,paradigm):
		self.paradigm = paradigm

	def clean(self):
		self.array = []
		self.dict = {}


