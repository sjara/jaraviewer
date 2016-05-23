from flask import Flask, render_template, redirect
from subprocess import call
from flask import request
import os
import numpy

#import ArraData as ad	#File for arrange data
import back_end_extend as bee
#import plot_py	#File for ploting

#plot_file = "plot.html"	#File name for the next page
#plot_path = "./plot_path"	#path for the plot that generated

app = Flask(__name__
			#, static_url_path = '/'
			, static_folder = 'static'
			)

#Read the homepage
@app.route('/')
@app.route('/jaraviewer')
def initial():
 
    mice = []
    mice = bee.get_mice()	#open the 'subject.txt'
    mice_str = ""
    mice_str = bee.format_index(mic=mice)	#get the html string
	
    #return render_template('home.html',test=mice_input,mice_num=mice_num)
    return render_template('home.html',test=mice_str)
	

#Get the information from the home page and excute the plot generator program
@app.route('/execute',methods=['POST'])
def execute():
    
    miceSelect = request.form.getlist('subject')
    #print miceSelect
    plot_type_list = request.form.getlist('plotType')
    #print plotType
    dateRange = request.form['dateRange']
    #print dateRange
    colum = request.form['columNum']
    #print colum
	
    date_list = []
    date_list = bee.date_generator(raw_date_str = dateRange)	#get the list of dates
    plot_file_name = []
    plot_file_name = bee.get_plot(miceSelect,date_list,plo_typ=plot_type_list)	#get the list of file names
	
    link_str = bee.link_gene(plo_fil_nam=plot_file_name,col=colum)	#get he string for sharing link
    return redirect(link_str,code=302)

#Show the page with the plots
@app.route('/link',methods=['GET'])
def link():
    #get arguments
    num = request.args.get('num')
    col = request.args.get('col')
    new_plot_list = []
    for i in range(0,int(num)):
        arg_name = "plot"+str(i)
        new_plot_list.append(request.args.get(arg_name))
	
    plot_str = bee.plot_render(plo_fil_nam=new_plot_list,col=col)	#get he string to render the html
    return render_template('back_static_flot.html',mou_str=plot_str)
	
	
if __name__ == "__main__":
    app.run(debug=True,port=5000)
