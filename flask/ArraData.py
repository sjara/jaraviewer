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
		graphDict = {}
		filename = ""




		for pt in self.PlotType:

			for d in self.data:
				
				mousename = d.session['subject']				
				time = d.session['date']
				date = d.session['date']
				year = date[0:4]
				month = date[5:7]
				day = date[8:10]
				date =  "_"+year+month+day+"_"
				filename = mousename+date+pt+".svg"

				graphDict['type'] = pt
				graphDict['filename'] = filename
				graphDict['data'] = self.data

				self.array.append(graphDict)
		print self.array
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


