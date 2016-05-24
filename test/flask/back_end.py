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
    profile = []
    profile = bee.read_profile()	#function for profiles
    
    return render_template('back_index.html',mice=mice_str,list_profiles=profile)
	

#Get the information from the home page and excute the plot generator program
@app.route('/execute',methods=['POST'])
def execute():

    save = request.form.getlist('save')	#check box for save

    miceSelect = request.form.getlist('subject')

    plot_type_list = request.form.getlist('plotType')

    dateRange = request.form['dateRange']

    colum = str(request.form['columNum'])
	
    #see if user choose save
    if len(save) > 0:
        save = str(save[0])
        if save == "Save":
            bee.write_profile(mic_lis=miceSelect,plo_lis=plot_type_list,dat_ran=dateRange,col=colum)	#write code to the profile.txt
            return redirect("/jaraviewer",code=302)

    #else
    date_list = []
    date_list = bee.date_generator(raw_date_str = dateRange)	#get the list of dates
    plot_file_name = []
    plot_file_name = bee.get_plot(miceSelect,date_list,plo_typ=plot_type_list)	#get the list of file names
	
    link_str = bee.link_gene(plo_fil_nam=plot_file_name,col=colum)	#get he string for sharing link
    return redirect(link_str,code=302)

#Show the page with the plots
@app.route('/link',methods=['GET'])
def link():
    num = request.args.get('num')
    col = request.args.get('col')
    new_plot_list = []
    for i in range(0,int(num)):
        arg_name = "plot"+str(i)
        new_plot_list.append(request.args.get(arg_name))
	
    plot_str = bee.plot_render(plo_fil_nam=new_plot_list,col=col)	#get he string to render the html
    return render_template('back_static_plot.html',mou_str=plot_str)
	
# Modify subjects (add/delete)
@app.route('/modify',methods=['POST'])
def modify():
    sub_str = request.form['subject']
    result = True
    if request.form['submit'] == "add":
        result = bee.add_subject(sub=sub_str)	#function for adding one subject to the subject.txt
    elif request.form['submit'] == "delete":
        result = bee.del_subject(sub=sub_str)	#function for deleting one subject from the subject.txt
    else:
        print "Error"
        return redirect("/jaraviewer",code=302)

        if result == False:
            print "Error"
		
    return redirect("/jaraviewer",code=302)


	
	
	
	
# Rendering the profile page
@app.route('/modify_saved_profile')
def modify_profile():
    profile = bee.read_profile()	#read from file
    pro_str = bee.format_profile(profile)	#rerenderthe html file
    return render_template('modify-saved-profile.html',profile=pro_str)

#Delete from profile.txt
@app.route('/delete_profile',methods=['POST'])
def delete_profile():
    check_list = request.form.getlist('profile')	#see which profile the user choose
    bee.dele_profile(index_list=check_list)	#delete from file
    return redirect("/jaraviewer",code=302)

	
'''
@app.route('/reset')
def reset():
    bee.reset_pro()
    return redirect("/jaraviewer",code=302)
'''
	
if __name__ == "__main__":
    app.run(debug=True,port=5000)
