#!/usr/bin/env python

'''
Main application that uses Flask to receive requests from the fron-end and renders the results page.
'''

import os
import numpy
import flask
import jinja2

#from jaraviewer import backend
#from jaraviewer import settings
import backend  ### ONLY DURING TESTING
import settings ### ONLY DURING TESTING

port_name = settings.JARAVIEWER_PORT_NAME
port_number = settings.JARAVIEWER_PORT_NUMBER

### fixed variables ###
trans_code = 302
home_page = 'index.html'
plot_page = 'plots_fixed.html'
modify_page = 'modify-saved-profile.html'

app = flask.Flask(__name__
					,static_folder = 'static'	#One method for leading the image path
					)

#Another method for leading the image path
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 
my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(APP_ROOT),
    ])
app.jinja_loader = my_loader

# -- Read the homepage --
@app.route(port_name)
def initial():
    '''
    Initial function. Load the data from subject file and profile file, and render the index.html.
    '''
    mice = backend.get_mice()	          # open the 'subject.txt'
    mice_str = backend.format_index(mic=mice) # get the html string
    profile = backend.read_profile()	  # function for profiles
    return flask.render_template(home_page, mice=mice_str, list_profiles=profile)


# -- Get the information from the home page and excute the plot generator program --
@app.route('/execute',methods=['POST'])
def execute():
    '''
    Method for excute the main code, including loading data and generate the plots.
    '''
    #save = flask.request.form.getlist('save')
    miceSelect = flask.request.form.getlist('subject')
    plot_type_list = flask.request.form.getlist('plotType')
    dateRange = flask.request.form['dateRange']
    colum = str(flask.request.form['columNum'])

    # -- Check if user chose save --
    if flask.request.form['submit'] == "saveProfile":
        # -- Write code to the profiles file --
        backend.write_profile(mic_lis=miceSelect,
                              plo_lis=plot_type_list,
                              dat_ran=dateRange,col=colum)
        return flask.redirect(port_name,code=trans_code)
    else:
        date_list = backend.date_generator(raw_date_str = dateRange)                      # Get the list of dates
        plot_file_name = backend.get_plot(miceSelect, date_list, plo_typ=plot_type_list)  # Get the list of file names
        link_str = backend.link_gene(plo_fil_nam=plot_file_name,col=colum)	          # Get the string for sharing link
        return flask.redirect(link_str,code=trans_code)


# -- Show the page with the plots --
@app.route('/link',methods=['GET'])
def link():
    num = flask.request.args.get('num')
    col = flask.request.args.get('col')
    new_plot_list = []
    for ind in range(0,int(num)):
        arg_name = "plot"+str(ind)
        new_plot_list.append(flask.request.args.get(arg_name))

    plot_str = backend.plot_render(plo_fil_nam=new_plot_list,col=col)	#get he string to render the html
    return flask.render_template(plot_page,mou_str=plot_str)


# -- Modify subjects (add/delete) --
@app.route('/modify',methods=['POST'])
def modify():
    sub_str = flask.request.form['subject']
    result = True
    if flask.request.form['submit'] == "add":
        result = backend.add_subject(sub=sub_str)	# Add one subject to subjects file
    elif flask.request.form['submit'] == "delete":
        result = backend.del_subject(sub=sub_str)	# Delete one subject from subjects file
    else:
        print "Error"
        return flask.redirect(port_name,code=trans_code)
        if result == False:
            print "Error"
    return flask.redirect(port_name,code=trans_code)

'''
# -- Render the profile page --
@app.route('/modify_saved_profile')
def modify_profile():
    profile = backend.read_profile()	        # Read from file
    pro_str = backend.format_profile(profile)   # Re-render the html file
    return flask.render_template(modify_page, profile=pro_str)
'''

# -- Delete from profiles file --
@app.route('/delete_profile',methods=['POST'])
def delete_profile():
    check_list = flask.request.form.getlist('profile')	# See which profile the user choose
    backend.dele_profile(index_list=check_list)	        # Delete from file
    return flask.redirect(port_name,code=trans_code)

if __name__ == "__main__":
    app.run(debug=True,port=port_number)
