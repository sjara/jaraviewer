from flask import Flask, render_template, redirect
from subprocess import call
from flask import request
import os
import numpy

#import ArraData as ad	#File for arrange data
import back_end_extend as bee
#import plotgenerator as pg	#File for ploting

#plot_file = "plot.html"	#File name for the next page
#plot_path = "./plot_path"	#path for the plot that generated

app = Flask(__name__
			#, static_url_path = '/'
			, static_folder = 'static'
			)

#modify_str = ""
			
#Read the homepage
@app.route('/')
@app.route('/jaraviewer')
def initial():
 
    mice = []
    mice = bee.get_mice()	#open the 'subject.txt'
    mice_str = ""
    mice_str = bee.format_index(mic=mice)	#get the html string
	
    #return render_template('home.html',test=mice_input,mice_num=mice_num)
    return render_template('back_index.html',mice=mice_str)
	

#Get the information from the home page and excute the plot generator program
@app.route('/execute',methods=['POST'])
def execute():
    #projectpath = request.form.save-profile-btn
    #print projectpath
    save = request.form.getlist('save')
    miceSelect = request.form.getlist('subject')
    #print miceSelect
    plot_type_list = request.form.getlist('plotType')
    #print plotType
    dateRange = request.form['dateRange']
    #print dateRange
    colum = request.form['columNum']
    #print colum
    if len(save) > 0:
        save = str(save[0])
        if save == "Save":
            #print "!!!!!!!!!!"
            bee.write_profile(mic_lis=miceSelect,plo_lis=plot_type_list,dat_ran=dateRange,col=colum)
            return redirect("/jaraviewer",code=302)

    #print save
    #print "save"

	
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
	
@app.route('/modify',methods=['POST'])
def modify():
    add = request.form['add_sub']
    dele = request.form['del_sub']
    add_result = True
    if not add=="":
        add_result = bee.add_subject(sub=add)
        if add_result == False:
            print "adding error"
    del_result = True
    if not dele=="":
        del_result = bee.del_subject(sub=dele)
        if del_result == False:
            print "deleting error"
    
        
    #print add_result
    #print add,dele
    return redirect("/jaraviewer",code=302)

@app.route('/reset')
def reset():
    bee.reset_pro()
    return redirect("/jaraviewer",code=302)
	
if __name__ == "__main__":
    app.run(debug=True,port=5000)
