#!/usr/bin python
from flask import Flask, render_template
from subprocess import call
from flask import request
import os

app = Flask(__name__
			#, static_url_path = "/image" #Path for the images that we will generate
			#, static_folder = "image"	#Folder for the images that we will generate
			)


#plotpy = "plotpy.py"	#Name for the plot generator program

#Read the homepage
@app.route('/')
@app.route('/home.html')
def initial():
    return render_template('home.html')
	
	

#Get the information from the home page and excute the plot generator program and read the image pathes for next website
@app.route('/execute',methods=['POST'])
def execute():
    
	#get the mice information
    miceSelect = request.form['miceSelect']
    #print miceSelect

	#get the plotType information
    plotType = request.form['plotType']
    #print plotType
	
    format_str = str(miceSelect) + str(plotType)	#Format the information here.
	
    #call(["python",plotpy,format_str])	#Excute the plot generator with arguments
    
	#Iterate the images.
    file_list = []
    file_counter = 0
	
    list_dirs = os.walk("./") 
    for root, dirs, files in list_dirs:
        for f in files:
            path = os.path.join(root, f)
            suffix = (os.path.splitext(f))[-1]
            if ".jpg" == suffix:
                file_counter += 1
                file_list.append(path)
	
	
	#Render the next website with the images.
    #return render_template('plot.html', file_counter=file_counter, file_list=file_list)
	
	
	return (format_str);
	


if __name__ == "__main__":
    app.run()

