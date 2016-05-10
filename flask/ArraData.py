import loadbehavior
import behavioranalysis
import numpy as np
import sys,os

class ArraData:

	array = []
	svg_array = []
	data = None
	PlotType = None
	
	file_path = ""
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
		
		
		self.clean()
		filename = ""
		
		print "len of bdata: "+str(len(self.data))
		
		list_dirs = os.walk("./image/")
		

		for pt in self.PlotType:

			for d in self.data:
				graphDict = {}
				mousename = d.session['subject']
				print "mouse name: "+str(mousename)
				date = d.session['date']
				year = date[0:4]
				month = date[5:7]
				day = date[8:10]
				date =  "_"+year+month+day+"_"
				filename = mousename+date+pt+".svg"

				graphDict['type'] = pt
				graphDict['filename'] = filename
				#self.graphDict['data'] = self.data
				
				self.svg_array.append(filename)
				
				check_file_exsits = False
				
				for root,dirs,files in list_dirs:
					if check_file_exsits:
						break
						
					for f in files:
						if f == filename:
							check_file_exsits = True
							break
				
				if not check_file_exsits:
					print "graphDict file name:"+str(graphDict['filename'])
					self.array.append(graphDict)
					print "self array: "+str(self.array)
					check_file_exsits = False
		
		print "array: "+str(self.array)
		print "len: "+str(len(self.array))
		temp_array = self.array
		temp_svg_array = self.svg_array
		
		
		
		
		
		return temp_array,temp_svg_array

		
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

		
	def set_path(self,file_path):
		self.file_path = file_path
		
	def clean(self):
		print "clean has been called"
		self.array = []
		self.svg_array = []


