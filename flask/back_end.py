#import jaratoolbox	#will import the jaratoolbox later
from flask import Flask, render_template
from subprocess import call
from flask import request
import os
import numpy

#import read_data
import ArraData as ad	#File for arrange data
import back_end_extend as bee
#import plot_py	#File for ploting

#polt_file = "plot.html"	#File name for the next page

app = Flask(__name__)

#Read the homepage
@app.route('/')
@app.route('/home.html')
def initial():
    return render_template('home.html')
	
	

#Get the information from the home page and excute the plot generator program and read the image pathes for next website
@app.route('/execute',methods=['POST'])
def execute():
    
	#get the mice information
    #miceSelect = str(request.form['miceSelect'])

    miceSelect = request.form.getlist('subject')
    #print miceSelect
    plotType = request.form.getlist('plotType')
    #print plotType
    dateRange = request.form['dateRange']
    #print dateRange
	
    #START_YEAR_STAR = 0
    #START_YEAR_END = 4
    #sta_year = dateRange[START_YEAR_STAR:START_YEAR_END]
    #print sta_year
    #mo = dateRange[5:7]
    #print mo
    #end_yea = dateRange[13:17]
    #print end_yea
    date_list = []
    date_list = bee.date_generator(raw_date_str = dateRange)
    raw_data_list = []
    raw_data_list = bee.get_data(miceSelect,date_list)
    
    AData = ad.ArraData(Data=raw_data_list,PlotType=plotType)
    plotList = AData.analyze_data()
	
    #print "{miceSelect}, {plotType}".format(miceSelect=miceSelect,plotType=plotType)

	#get the plotType information
    #plotType = request.form['plotType']
    #print plotType
	
    #format_str = str(miceSelect) + str(plotType)	#Format the information here.

    #info_arr = numpy.array([miceSelect])
    #print info_arr
	
    #raw_data = read_data.get_data(data_arra = info_arr)	#Read the raw data that needed

    #print raw_data
	
	#########################test Arrange data#######################
    
	
    #arra_data = ad.ArraData(Data=raw_data)	#Arrange the raw data
    #arra_data.set_name(miceSelect)
    #arra_data.set_session(dateRange)
    #arra_data.set_paradigm(plotType)
	
    #arra_data.arrange_data(plot_type=plotType)
    
    
	
    #ready_data = arra_data.get_array()
	#########################test Arrange data#######################

	#Generrate the file for different plot types
    if plotType == "psychometric":
        pass   
        #plot_py.plot_psychometric(good_data)
    elif plotType == "summary":
        #plot_py.plot_summary(good_data)
        pass
    elif plotType == "dynamics":
        #plot_py.plot_dynamics(good_data)
        pass


	#Return the html file that generated.
    #return render_template(polt_file)

    #print be_data
    #display = "behavData=<br><br>{raw_data}<br><br>arrangeData=<br><br>{ready_data}".format(raw_data=raw_data,ready_data=ready_data)
    #return display
    display = "{plotList}".format(plotList=plotList)
    return display

if __name__ == "__main__":
    app.run(debug=True,port=5000)
