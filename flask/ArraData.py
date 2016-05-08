import loadbehavior
import behavioranalysis
import numpy as np
class ArraData:

	array = []
	data = None
	PlotType = None
	dict = {}
	name = ""
	session = ""
	paradigm = ""
	#init the class
	def __init__(self,Data,PlotType):
		#get the behavior data from here
		self.data = Data
		self.PlotType = PlotType
		
	
	#main function, return an particular array to the plot builder
	def analyze_data(self):
		#self.dict['name'] = self.name
		#self.dict['choice'] = self.data['choice']
		#self.dict['session'] = self.data.session
		#self.dict['paradigm'] = self.paradigm
		#self.dict['title'] = 'My plot'
		#self.dict['ciHitsEachValue'] = []




		for pt in self.PlotType:
			#analyze the data and slice the info to build a psychometric graph
			if pt == 'psychometric':
				for d in self.data:
					print "arrange psychometric data"
					(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = 						behavioranalysis.calculate_psychometric(d['choice']
					,d['targetFrequency'],d['valid'])
					

					pltDict1 = {'type':'psychometric','title':'My plot','possibleValues':possibleValues,
'fractionHitsEachValue':fractionHitsEachValue,'ciHitsEachValue':ciHitsEachValue,'mouse name':d.session['subject']}
					print pltDict1
					self.array.append(pltDict1)
				
			#analyze the data and slice the info to build a summary graph
			elif pt == 'summary':
				print "arrange summary data"
				self.dict['plot_type'] = 'summary'
				self.array.append(self.dict)

			#analyze the data and slice the info to build a dynamics graph
			elif pt == 'dynamics':
				print "arrange dynamics data"
				self.dict['plot_type'] = 'dynamics'
				self.array.append(self.dict)

			# type not found
			else:
				print "no this type of plot"

		return self.array

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


