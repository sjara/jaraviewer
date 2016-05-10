#import jaratoolbox	#will import the jaratoolbox later
from flask import Flask, render_template
from subprocess import call
from flask import request
import os
import numpy

import ArraData as ad	#File for arrange data
import back_end_extend as bee
#import plot_py	#File for ploting

#plot_file = "plot.html"	#File name for the next page
#plot_path = "./plot_path"	#path for the plot that generated

app = Flask(__name__)

#Read the homepage
@app.route('/')
@app.route('/home.html')
def initial():
    
    mice = []
	
    try:
        mice_file = open("./static/data/subjects.txt","r")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    #print mice
    mouse_str = ""
    count = 1
    is_break = ""
    for mouse in mice:
        if count%4 == 0:
            is_break = "<br>"
        mouse_str += "<input type ='checkbox' id='subject{count1}' name='subject' value='{subj1}' class='hidden_subject'>	<label class='label_subject btn btn-primary' for='subject{count2}'>	<div class='label_name'>{subj2}</div>	</label> {is_bre}".format(count1=count,subj1=mouse,count2=count,subj2=mouse,is_bre=is_break)
        count += 1
        is_break = ""
    print mouse_str
	
    #return render_template('home.html',test=mice_input,mice_num=mice_num)
    return render_template('home.html',test=mouse_str)
	

#Get the information from the home page and excute the plot generator program and read the image pathes for next website
@app.route('/execute',methods=['POST'])
def execute():
    
    miceSelect = request.form.getlist('subject')
    #print miceSelect
    plot_type_list = request.form.getlist('plotType')
    #print plotType
    dateRange = request.form['dateRange']
    #print dateRange
	
    date_list = []
    date_list = bee.date_generator(raw_date_str = dateRange)
    raw_data_list = []
    raw_data_list = bee.get_data(miceSelect,date_list)
    
    AData = ad.ArraData(Data=raw_data_list,PlotType=plot_type_list)
    plotList,imageList = AData.analyze_data()
	

    display = "plotList: {plotList} <br>imageList: {imageList} ".format(plotList=plotList,imageList=imageList)
    return display

if __name__ == "__main__":
    app.run(debug=True,port=5000)
