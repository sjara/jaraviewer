'''
This is the back-end module.
All the functions that related to the back-end will be defined here.
'''

import datetime
import time
import sys
import os
import shutil

from jaratoolbox import loadbehavior

from jaraviewer import settings
from jaraviewer import plotgenerator as pg	#File for ploting

# -- Fixed parameters --
PARADIGM = '2afc'         # Behavioral paradigm
SUBJECTS_PER_ROW = 5      # Number of buttons per line

# -- Old parameters --
#link_tag = '/link'        #tag name for sharing link and rendering plots function, need to change the 'link_tag' in 'jaraviewerapp.py' if this is changed
#static_group_width = 200  # Width of  to show the group name in static mode
#make_up_br = 200          # leaving a little more space horizontally for static mode

# -- Indexes for extracting the date --
START_YEAR_STA = 0
START_YEAR_END = 4
START_MONTH_STA = 5
START_MONTH_END = 7
START_DAY_STA = 8
START_DAY_END = 10
END_YEAR_STA = 13
END_YEAR_END = 17
END_MONTH_STA = 18
END_MONTH_END = 20
END_DAY_STA = 21
END_DAY_END = 23


def read_subjects(filename=settings.SUBJECTS_FILE):
    '''
    Read list of subjects from a file.

    Args:
        filename (str): full path to the file containing subjects.
    Returns:
        subjects (list): list of strings with subject names.
    '''
    # FIXME: this is a weird way to test the file exists and create it otherwise
    try:
        mice_file = open(filename,"r")
    except:
        mice_file = open(filename,"w")
        mice_file.close()
        mice_file = open(filename,"r")
    subjects = mice_file.read().splitlines()
    mice_file.close()
    return subjects
	

def subjects_buttons(subjects):
    '''
    Generate HTML for subject buttons.

    Args:
        subjects (list): list of strings with subject names.
    Returns:
        mouse_str: HTML string for rendering the mice checkbox.
    '''
    mouse_str = ""
    count = 1
    is_break = ""
    for mouse in subjects:
        if count%SUBJECTS_PER_ROW == 0:
            is_break = "<br>"
        mouse_str += "<input type='checkbox' id='{sub}' name='subject' value='{subj1}' class='hidden_subject'>\n".format(sub=mouse,subj1=mouse)
        mouse_str += "<label class='label_subject btn btn-primary' for='{sub2}'>\n".format(sub2=mouse)
        mouse_str += "{subj2}</label>{is_bre}\n".format(subj2=mouse,is_bre=is_break)
        count += 1
        is_break = ""
    return mouse_str

#get all the dates from the date string
def date_generator(raw_date_str):
    '''
    Args:
        raw_date_str: A string to store the date range.
    Returns:
        date_list: A list to store all the dates between the date range
    '''
    star_year = int(raw_date_str[START_YEAR_STA:START_YEAR_END])
    star_month = int(raw_date_str[START_MONTH_STA:START_MONTH_END])
    star_day = int(raw_date_str[START_DAY_STA:START_DAY_END])
    end_year = int(raw_date_str[END_YEAR_STA:END_YEAR_END])
    end_month = int(raw_date_str[END_MONTH_STA:END_MONTH_END])
    end_day = int(raw_date_str[END_DAY_STA:END_DAY_END])
    start_date = datetime.date(star_year,star_month,star_day)
    end_date = datetime.date(end_year,end_month,end_day)
    
    date_list = []
    temp_date = start_date
    delta = end_date - start_date
    delta = int(delta.days)
    for i in range(0,delta+1):
        date_str = temp_date.strftime("%Y%m%d")
        date_str = date_str + 'a'
        date_list.append(date_str)
        temp_date += datetime.timedelta(days=1)
    return date_list
	

#link to the plot module
def create_plots(subjectsList, datesList, plotsList):
    '''
    Return a list of plots filenames.

    Args:
        subjectsList (list): list of strings with subject names.
        datesList (list): list of strings with sessions.
        plotsList (list): list of strings with plot names.
    Returns:
        allFilenames (list): all the filenames of plots.
    '''
    allFilenames = []
    for subject in subjectsList:
        for session in datesList:
            behavData = None
            # FIXME: specify an exception type
            try:
                behavFile = loadbehavior.path_to_behavior_data(subject, PARADIGM, session)
                behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
            except:
                for plot_type in plotsList:
                    out_dict = form_out_put(sub=subject,typ='summary',data=None,sess=session)
                    allFilenames.append(out_dict['filename'])
                continue
            for plot_type in plotsList:
                out_dict = form_out_put(subject, plot_type, behavData, session)
                allFilenames.append(out_dict['filename'])
                if settings.REGENERATE_PLOTS:
                    pg.generate(out_dict, settings.IMAGE_PATH)
                else:
                    if not os.path.isfile(out_dict['filename']):
                        pg.generate(out_dict, settings.IMAGE_PATH)
    return allFilenames


#form a dictionary for the ploting function
def form_out_put(sub,typ,data,sess):
    '''
    Args:
        sub: A string for one mouse
        date: A string for one date
        typ: A string for one plot type
    Returns:
        out_dict: A dictionary that contains all the information for one plot
    '''
    out_dict = {}
    out_dict['type'] = str(typ)
    form_sess = sess[0:-1]
    out_dict['filename'] = str(sub)+'_'+str(form_sess)+'_'+str(typ)+'.svg'
    out_dict['data'] = data
    return out_dict


#generate the string of html for showing plot page
def plot_render(plots_filenames, col):
    '''
    Generate the HTML for the plots section of the output page.

    Args:
        plots_filenames: A list to store the plot file name
        col: column number from the front-end
    Returns:
        plot_str: HTML string for rendering the plots.
    '''
    sessionsList = []
    plotsLabels = []
    plotsItems = []
    for onePlotFilename in plots_filenames:
        (subject,datestr,plotype) = onePlotFilename.split('_',3)
        plotLabel = '{0} [{1}]'.format(subject,datestr)
        sessionKey = subject+datestr
        # NOTE: this looks almost like a dict, but it is sorted.
        if sessionKey not in sessionsList:
            sessionsList.append(sessionKey)
            plotsItems.append([])
            plotsLabels.append(plotLabel)
        sessionInd = sessionsList.index(sessionKey)
        plotsItems[sessionInd].append(onePlotFilename)
    type_number = len(plotsItems[sessionInd]) # Number of plots per session?

    # -- Case for dynamic --
    if col == '-':
        plot_str = ""
        for sessionInd,plotItems in enumerate(plotsItems):
            gro_str  = "  <div class='session_group'>\n"
            gro_str += "    <div class='session_title'>{0}</div>\n".format(plotsLabels[sessionInd])
            gro_str += "    <div class='img_group'>"
            for plotFilename in plotsItems[sessionInd]:
                imgfilepath = os.path.join(settings.IMAGE_PATH,plotFilename)
                # FIXME: hard-coded path
                #imgfilepath = os.path.join('/jaraviewer/static/output/',plotFilename)
                gro_str += "        <img src={0} alt=''>\n".format(imgfilepath)
            gro_str += "    </div>\n"
            gro_str += "  </div>\n\n"
            plot_str += gro_str
    return plot_str

    '''
    #case for static
    col = int(col)
    if col > 0:
        css_f = open('./static/static_plot.css','r')
        for line in css_f:
            if '--widthX' in line:
                im_width = line.split()
                #print test
                im_width = int(im_width[1][0:-3])
                print im_width
                break

        width = col*((static_group_width*type_number)+im_width+make_up_br)
        width = str(width)
        col_counter = 0
        plot_str = ""+"<table cellpadding='0' cellspacing='0' border='0'> <tr class='row1'>"
        for group in mice_date:
            if col_counter < col:
                group_str = ""
                group_str += "<td><h1 style='width:"+str(static_group_width)+"px'>"+group+"</h1></td>"
                for file_name in mice_date[group]:
                    ima_src = ""
                    ima_src = os.path.join(ima_src,settings.IMAGE_PATH)
                    ima_src = os.path.join(ima_src,file_name)
                    group_str += "<td><img src='"+ima_src+"' /></td>"
                group_str += "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                plot_str += group_str
                col_counter += 1
            elif col_counter >= col:
                plot_str += "</tr> </table> <br> <hr style='width: "+width+"px' />"
                plot_str += "<table cellpadding='0' cellspacing='0' border='0'> <tr class='row1'>"
                group_str = ""
                group_str += "<td><h1 style='width:"+str(static_group_width)+"px;left: 0; top: 2'>"+group+"</h1></td>"
                for file_name in mice_date[group]:
                    ima_src = ""
                    ima_src = os.path.join(ima_src,settings.IMAGE_PATH)
                    ima_src = os.path.join(ima_src,file_name)
                    group_str += "<td><img src='"+ima_src+"' /></td>"
                group_str += "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                plot_str += group_str                
                col_counter = 1
        plot_str += "</tr> </table> <br> <hr style='width: "+width+"px' />"
    return plot_str
    '''
	

def output_args(plotsFilenames, col):
    '''
    Generate arguments of the URL for the results page.

    Args:
        plotsFilenames: A list to store the plot file name
        col: column number from the front-end
    Returns:
        link_str: URL for showing the plots, also for share
    '''
    argdict = {}
    for indp, plotName in enumerate(plotsFilenames):
        argdict['plot{0}'.format(indp)] = plotName
    argdict['num'] = str(len(plotsFilenames))
    argdict['col'] = str(col)
    return argdict

def link_gene__OBSOLETE(plotsFilenames, col):
    '''
    Generate the URL for the results page.

    Args:
        plotsFilenames: A list to store the plot file name
        col: column number from the front-end
    Returns:
        link_str: URL for showing the plots, also for share
    '''
    link_str = link_tag + '?'
    count = 0
    for plot_name in plotsFilenames:
        temp_str = "plot"+str(count)+"="+plot_name+'&'
        link_str += temp_str
        count +=1
    link_str += "num="+str(count)
    link_str += "&col=" + str(col)
    return link_str


def add_subject(subject, filename=settings.SUBJECTS_FILE):
    '''
    Add a subject to the subjects file.
    
    Args:
        subject (str): name of the subject to add.
        filename (str): full path to the file containing subjects.
    Returns:
        (bool): True=success, False=failed to add subject.
    '''
    try:
        mice_file = open(filename,"r+")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    if subject in mice:
        return False
    subject += '\n'
    mice_file.close()
    try:
        mice_file = open(filename,"a+")
    except:
        print "Can't open the file"
    mice_file.write(subject)
    mice_file.close()
    return True

#function for deleting subject
def del_subject(subject):
    '''
    Args:
        subject: A string for the mouse name to delete
    Returns:
        1. False: Failed to delete the mouse
        2. True: Successfully deleting the mouse
    '''
    file_path = settings.SUBJECTS_FILE
    try:
        mice_file = open(file_path,"r")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    try:
        mice.remove(subject)
    except:
        return False
    mice_file.close()
    temp_path = file_path+".new"
    print temp_path
    loop_count = 0
    while (os.path.isfile(temp_path)):
        time.sleep(1)
        print "Wait for another user!"
        if loop_count > 5:
            os.remove(temp_path)
        loop_count += 1
    try:
        temp_file = open(temp_path,'w')
    except:
        print "Can't open file"
    for mouse in mice:
        mouse += '\n'
        temp_file.write(mouse)
    temp_file.close()
    shutil.move(temp_path, file_path)
    return True
	

def save_profile(subjectsList, plotsList):
    '''
    Save a profile.

    Args:
        subjectsList (list): each item is the name of a subject.
        plotsList (list): each item is the name of a plot.
    '''
    profileStr = ','.join(subjectsList) + ';' + ','.join(plotsList) + '\n'
    pFile = open(settings.PROFILES_FILE,'a+')
    pFile.write(profileStr)
    pFile.close()


def read_profiles(filename=settings.PROFILES_FILE):
    '''
    Read profiles from a file.

    Args:
        filename (str): full path to the file containing subjects.
    Returns:
        res_list: A list contains all the profile information
    '''
    # FIXME: this is a weird way to test the file exists and create it otherwise
    try:
        pFile = open(filename,'r')
    except:
        pFile = open(filename,'w')
        pFile.close()
        pFile = open(filename,'r+')
    resList = []
    proList = pFile.read().splitlines()
    pFile.close()
    index = 0
    for indp,prof in enumerate(proList):
        profData = prof.split(';')
        mice = profData[0].split(',')
        plots = profData[1].split(',')
        profDict = {'index':str(indp), 'subject':mice, 'plotType':plots}
        resList.append(profDict)
    return resList


#function to generate the strings of html for profile selecting, not done
def format_profile(profile_list):
    '''
    Args:
        profile_list: A list contains all the profile information
    Returns:
        profile_str: HTML string to renter the profile part
    '''
    profile_str = ""
    count = 1
    is_break = ""
    for profile in profile_list:
        one_pro_str = ""
        one_pro_str += profile['index']
        print one_pro_str,profile['index']
        one_pro_str += "<br>"
        #one_pro_str += str(profile['subject'])
        for sub in profile['subject']:
            one_pro_str += sub
            one_pro_str += ', '
        print one_pro_str,profile['index']
        one_pro_str += "<br>"
        #one_pro_str += str(profile['plotType'])
        for plot in profile['plotType']:
            one_pro_str += plot
            one_pro_str += ', '
        print one_pro_str,profile['index']
        is_break = "<br>"
        profile_str += "<input type ='checkbox' id='{index1}' name='profile' value='{index2}' class='hidden_profile'>	<label class='label_profile' for='{index3}'>	<div class='label_name'>{prof}</div>	</label> {is_bre}".format(index1=str(profile['index']),index2=str(profile['index']),index3=str(profile['index']),prof=one_pro_str,is_bre=is_break)
        count += 1
    return profile_str
	
	
	
# function to delete profile
def dele_profile(index_list):
    '''
    Args:
        index_list: A list contains all the profile index to delete
    Returns:
        None
    '''
    str_index_list = []
    for index in index_list:
        str_index_list.append(str(index))
    file_path = settings.PROFILES_FILE
    try:
        profile = open(file_path,"r+")
    except:
        print "Can't open the file"
    old_pro_lis = profile.read().splitlines()
    profile.close()
	
    new_file_path = file_path+".new"
    loop_count = 0
    while (os.path.isfile(new_file_path)):
        time.sleep(1)
        print "Wait for another user!"
        if loop_count > 5:
            os.remove(new_file_path)
        loop_count += 1
    try:
        new_pro = open(new_file_path,"a+")
    except:
        print "Can't open the file"
    counter = 1
    for pro_str in old_pro_lis:
        if not str(counter) in str_index_list:
            pro_str += '\n'
            new_pro.write(pro_str)
        counter += 1
    new_pro.close()
    shutil.move(new_file_path, file_path)

	
def get_css_str(co):
    '''
    Args:
        co: column number from the front-end
    Returns:
        1. HTML string to render the CSS part.
    '''
    if co == '-':
        return "<link rel='stylesheet' type='text/css' href='./static/dynamic_plot.css'>"
    else:
        return "<link rel='stylesheet' type='text/css' href='./static/static_plot.css'>"
