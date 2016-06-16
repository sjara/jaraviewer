#!/usr/bin/env python

'''
Main application that uses Flask to receive requests from the fron-end and renders the results page.
'''


import flask
import os

from jaraviewer import backend
from jaraviewer import settings

# -- Get settings --
PORT_NAME = settings.JARAVIEWER_PORT_NAME	#tag name for 'initial' function
port_number = settings.JARAVIEWER_PORT_NUMBER	#port number for the jaraviewer
local_address = settings.JARAVIEWER_LOCAL_ADDRESS	#local address for the flask

# -- Define template locations --
TRANS_CODE = 302               # 302 for successfully transfer to another address
home_page = 'index.html'       # Main page template
plot_page = 'plots_fixed.html' # Results page template
modify_page = 'modify-saved-profile.html'  # Page for deleting profiles

link_tag = '/link'
# tag name for sharing link and rendering plots function,
# need to change the 'link_tag' in 'backend.py' if this is changed


app = flask.Flask(__name__, static_folder = 'static')


#@app.route(PORT_NAME)
@app.route('/')
def initial():
    '''
    Render the main page.

    Returns:
        The main page as HTML (including existing subjects and profiles)
    '''
    mice = backend.read_subjects()             # Load list of mice
    mice_str = backend.subjects_buttons(mice)  # Make html for buttons
    profile = backend.read_profiles()          # Load profiles
    return flask.render_template(home_page, location=PORT_NAME,
                                 mice=mice_str, list_profiles=profile)



@app.route('/execute',methods=['POST'])
def execute():
    '''
    Get parameters from main page and render plots.

    Returns:
        1.Redirect to the 'initial' function.
        2.Redirect to the 'link' function.
        TRANS_CODE: 302 for successly transfer to anther address
    '''
    save = flask.request.form.getlist('save')
    miceSelect = flask.request.form.getlist('subject')
    plot_type_list = flask.request.form.getlist('plotType')
    dateRange = flask.request.form['dateRange']
    colum = str(flask.request.form['columNum'])

    # -- Check if user chose SaveProfile --
    if flask.request.form['submit'] == 'saveProfile':
        backend.write_profile(mic_lis=miceSelect,
                              plo_lis=plot_type_list)
        return flask.redirect(PORT_NAME,code=TRANS_CODE)
    # -- Otherwise, user chose submit --
    else:
        date_list = backend.date_generator(raw_date_str = dateRange)                      # Get the list of dates
        plot_file_name = backend.get_plot(miceSelect, date_list, plo_typ=plot_type_list)  # Get the list of file names
        link_str = backend.link_gene(plo_fil_nam=plot_file_name,col=colum)	          # Get the string for sharing link
        return flask.redirect(link_str,code=TRANS_CODE)


# -- Show the page with the plots --
@app.route(link_tag,methods=['GET'])
def link():
    '''
    Args:
        None
    Returns:
        A rendered plot page.
        plot_str: HTML string for building up the plots
        css_str: CSS string for changing the style of plots
    '''
    num = flask.request.args.get('num')
    col = flask.request.args.get('col')
    new_plot_list = []
    for ind in range(0,int(num)):
        arg_name = "plot"+str(ind)
        new_plot_list.append(flask.request.args.get(arg_name))

    css_str = backend.get_css_str(co=col)
    plot_str = backend.plot_render(plo_fil_nam=new_plot_list,col=col)	#get he string to render the html
    return flask.render_template(plot_page,mou_str=plot_str,cs_str=css_str)


@app.route('/modify',methods=['POST'])
def modify():
    '''
    Modify list of subjects (add or delete).

    Returns:
        Redirect to main method 'initial'.
    '''
    sub_str = flask.request.form['subject']
    result = True
    if flask.request.form['submit'] == "add":
        result = backend.add_subject(sub_str)	# Add one subject to subjects file
    elif flask.request.form['submit'] == "delete":
        result = backend.del_subject(sub_str)	# Delete one subject from subjects file
    else:
        flask.abort(406) # Send code for "Not acceptable"
    return flask.redirect(flask.url_for('initial'))


# -- Render the profile page --
@app.route('/modify_saved_profile')
def modify_profile():
    '''
    Args:
        None
    Returns:
        A rendered modify profile page.
        pro_str: HTML string for building up profiles
    '''
    profile = backend.read_profile()	        # Read from file
    pro_str = backend.format_profile(profile)   # Re-render the html file
    return flask.render_template(modify_page, profile=pro_str)


# -- Delete from profiles file --
@app.route('/delete_profile',methods=['POST'])
def delete_profile():
    '''
    Args:
        None
    Returns:
        Redirect to the 'initial' function.
        TRANS_CODE: 302 for successly transfer to anther address
    '''
    check_list = flask.request.form.getlist('profile')	# See which profile the user choose
    backend.dele_profile(index_list=check_list)	        # Delete from file
    return flask.redirect(PORT_NAME,code=TRANS_CODE)

if __name__ == "__main__":
    app.run(host=local_address,debug=True,port=port_number)
