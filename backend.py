'''
This is the back-end module.
All the functions that related to the back-end will be defined here.
'''

import datetime
import time
import sys
import os
import shutil

import jaratoolbox
from jaratoolbox import loadbehavior

from jaraviewer import settings
from jaraviewer import plotgenerator as pg	#File for ploting

###fixed variable###
EXPERIMENTER = 'santiago'	#name for the EXPERIMENTER
paradigm = '2afc'	#name for the paradigm
static_group_width = 200	#width to show the group name in static mode
make_up_br = 200	#leaving a little more space horizontally for static mode
subject_br = 4	#the number of mice checkboxes will be showed in one line in the home page
link_tag = '/link'	#tag name for sharing link and rendering plots function, need to change the 'link_tag' in 'jaraviewerapp.py' if this is changed

#indexes for extracting the date 
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

#function to open 'subject.txt'
def get_mice():
    '''
    Args:
        None
    Returns:
        A list to store the mice
    '''
    mice = []
    try:
        mice_file = open(settings.SUBJECTS_FILE,"r")
    except:
        mice_file = open(settings.SUBJECTS_FILE,"w")
        mice_file.close()
        mice_file = open(settings.SUBJECTS_FILE,"r")
    mice = mice_file.read().splitlines()
    mice_file.close()
    return mice
	
#function to generate the strings of html for mouse selecting
def format_index(mic):
    '''
    Args:
        mic: A list to store the mice
    Returns:
        mouse_str: HTML string for rendering the mice checkbox
    '''
    mouse_str = ""
    count = 1
    is_break = ""
    for mouse in mic:
        if count%subject_br == 0:
            is_break = "<br>"
        mouse_str += "<input type ='checkbox' id='{sub}' name='subject' value='{subj1}' class='hidden_subject'>	<label class='label_subject btn btn-primary' for='{sub2}'>	<div class='label_name'>{subj2}</div>	</label> {is_bre}".format(sub=mouse,subj1=mouse,sub2=mouse,subj2=mouse,is_bre=is_break)
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
def get_plot(mice,date,plo_typ):
    '''
    Args:
        mice: A list to store the mice
        date: A list to store the dates
        plo_typ: A list to store the plot types
    Returns:
        all_file_name: A list to store all the file names that referenced in this excuction
    '''
    subject_list = mice
    session_list = date
	
    all_file_name = []
    for subject in subject_list:
        for session in session_list:
            behavData = None
            try:
                behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
                behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
            except:
                for plot_type in plo_typ:
                    out_dict = form_out_put(sub=subject,typ='summary',data=None,sess=session)
                    all_file_name.append(out_dict['filename'])
                continue
            for plot_type in plo_typ:
                out_dict = form_out_put(sub=subject,typ=plot_type,data=behavData,sess=session)
                all_file_name.append(out_dict['filename'])
                if not check_exist(fil_nam=out_dict['filename']):
                    #non_exsi_file.append(out_dict['filename'])
                    #test_list=[]
                    #test_list.append(out_dict)
                    pg.generate(out_dict, settings.IMAGE_PATH)
    return all_file_name






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

#function to check is the image already existed
def check_exist(fil_nam):
    '''
    Args:
        fil_nam: A string for the name of one plot file
    Returns:
        1. True: If the file name already exists in the folder
        2. False: If the file name not exists in the folder
    '''
    check_file_exists = False
    image_path = os.walk(settings.IMAGE_PATH)
    for root,dirs,files in image_path:
        if check_file_exists:
            return True
        for f in files:
            if f == fil_nam:
                check_file_exists = True
                return True
    if not check_file_exists:
        return False

#generate the string of html for showing plot page
def plot_render(plo_fil_nam,col):
    '''
    Args:
        plo_fil_nam: A list to store the plot file name
        col: column number from the front-end
    Returns:
        plot_str: HTML string for rendering the plots.
    '''
    mice_date = {}
    for plot in plo_fil_nam:
        stri = plot.split('_',3)
        mice_date_str = stri[0]+'-'+stri[1]
        if mice_date_str in mice_date.keys():
            mice_date[mice_date_str].append(plot)
        else:
            mice_date[mice_date_str] = []
            mice_date[mice_date_str].append(plot)
	
    type_number = len(mice_date[mice_date_str])
	
    #case for dynamic
    if col == '-':
        css_f = open('./static/dynamic_plot.css','r')
        for line in css_f:
            if '--widthX' in line:
                width = line.split()
                #print test
                width = int(width[1][0:-3])
                break
        counter = 0
        plot_str = ""

        for group in mice_date:
            ima_num = len(mice_date[group])
            style_wid = width*ima_num
            gro_str = ""
            gro_str += "<ul class='img_customer' style='width:"+str(style_wid)+"px'>"
            gro_str += "<p>"+group+"</p>"
            for img in mice_date[group]:
                ima_src = ""
                ima_src = os.path.join(ima_src,settings.IMAGE_PATH)
                ima_src = os.path.join(ima_src,img)
                ima_str = ""
                ima_str += "<li><img src="+ima_src+"></li>"
                gro_str += ima_str
            plot_str += gro_str
            plot_str += '</ul>'
        return plot_str

	
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
	
#generate the string of URL for sharing.
def link_gene(plo_fil_nam,col):
    '''
    Args:
        plo_fil_nam: A list to store the plot file name
        col: column number from the front-end
    Returns:
        link_str: URL for showing the plots, also for share
    '''
    link_str = link_tag + '?'
    count = 0
    for plot_name in plo_fil_nam:
        temp_str = "plot"+str(count)+"="+plot_name+'&'
        link_str += temp_str
        count +=1
    link_str += "num="+str(count)
    link_str += "&col=" + str(col)
    return link_str

#functon for adding subject
def add_subject(sub):
    '''
    Args:
        sub: A string for the mouse name to add
    Returns:
        1. False: Failed to add the mouse
        2. True: Successfully adding the mouse
    '''
    try:
        mice_file = open(settings.SUBJECTS_FILE,"r+")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    if sub in mice:
        return False
    sub += '\n'
    mice_file.close()
    try:
        mice_file = open(settings.SUBJECTS_FILE,"a+")
    except:
        print "Can't open the file"
    mice_file.write(sub)
    mice_file.close()
    return True

#function for deleting subject
def del_subject(sub):
    '''
    Args:
        sub: A string for the mouse name to delete
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
        mice.remove(sub)
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
	
#function for wirte profile
def write_profile(mic_lis,plo_lis):
    '''
    Args:
        mic_lis: A list to store the mice to add in the porfile
        plo_lis: A list to store the plot types to add in the porfile
    Returns:
        None
    '''
    profile = open(settings.PROFILES_FILE,'a+')
    wri_str = ""
    for mouse in mic_lis:
        mouse = str(mouse) + ','
        wri_str += mouse
    wri_str += ';'
    for plot in plo_lis:
        plot = str(plot) + ','
        wri_str += plot
    wri_str += '\n'
    while True:
        try:
            profile.write(wri_str)
            break
        except:
            time.sleep(1)
    profile.close()

#read profile from file
def read_profile():
    '''
    Args:
        None
    Returns:
        res_list: A list contains all the profile information
    '''
    try:
        profile = open(settings.PROFILES_FILE,'r')
    except:
        profile = open(settings.PROFILES_FILE,'w')
        profile.close()
        profile = profile = open(settings.PROFILES_FILE,'r+')
    res_list = []
    pro_list = profile.read().splitlines()
    profile.close()
    index = 0
    for prof in pro_list:
        pro_dict = {}
        pro_data = prof.split(';',1)
        mice = pro_data[0].split(',')
        mice = mice[0:-1]
        type_list = pro_data[1].split(',')
        type_list = type_list[0:-1]
        index += 1
        pro_dict['index'] = str(index)
        pro_dict['subject'] = mice
        pro_dict['plotType'] = type_list
        res_list.append(pro_dict)
    return res_list


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
