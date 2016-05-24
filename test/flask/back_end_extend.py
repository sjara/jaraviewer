import datetime
import time
import sys,os
import shutil

from jaratoolbox import loadbehavior
#import loadbehavior
import settings
import back_plotgenerator as pg	#File for ploting

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
    mice = []
    try:
        mice_file = open(settings.SUBJECT_PATH,"r")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    mice_file.close()
    return mice
	
#function to generate the strings of html for mouse selecting
def format_index(mic):
    mouse_str = ""
    count = 1
    is_break = ""
    for mouse in mic:
        if count%4 == 0:
            is_break = "<br>"
        mouse_str += "<input type ='checkbox' id='{sub}' name='subject' value='{subj1}' class='hidden_subject'>	<label class='label_subject btn btn-primary' for='{sub2}'>	<div class='label_name'>{subj2}</div>	</label> {is_bre}".format(sub=mouse,subj1=mouse,sub2=mouse,subj2=mouse,is_bre=is_break)
        count += 1
        is_break = ""
    return mouse_str

#get all the dates from the date string
def date_generator(raw_date_str):
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

    EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
    paradigm = '2afc'

    subject_list = mice
    session_list = date
	
    all_file_name = []
    for subject in subject_list:
        for session in session_list:
            behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
            behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
            for plot_type in plo_typ:
                out_dict = form_out_put(sub=subject,typ=plot_type,data=behavData,sess=session)
                all_file_name.append(out_dict['filename'])
                if not check_exsit(fil_nam=out_dict['filename']):
                    #non_exsi_file.append(out_dict['filename'])
                    test_list=[]
                    test_list.append(out_dict)
                    pg.Generate(plotList=test_list)
                    #test_plot(out_dic=out_dict)
                    #print
					

    return all_file_name


#form a dictionary for the ploting function
def form_out_put(sub,typ,data,sess):
    out_dict = {}
    out_dict['type'] = str(typ)
    form_sess = sess[0:-1]
    out_dict['filename'] = str(sub)+'_'+str(form_sess)+'_'+str(typ)+'.svg'
    out_dict['data'] = data
    return out_dict

#function to check is the image already exsited
def check_exsit(fil_nam):
    check_file_exsits = False
    image_path = os.walk(settings.IMAGE_PATH)
    for root,dirs,files in image_path:
        if check_file_exsits:
            return True
        for f in files:
            if f == fil_nam:
                check_file_exsits = True
                return True
    if not check_file_exsits:
        return False

'''		
def test_plot(out_dic):
    file_path = settings.IMAGE_PATH+out_dic['filename']
    f=open(file_path,'w+')
    f.close()
'''

#generate the string of html for showing plot page
def plot_render(plo_fil_nam,col):
    #print "!!!!!!!!!!!!!"
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
    counter = 0
    plot_str = ""
    plot_str += "<div class='row'>"
    if col == '-':
        for group in mice_date:
            if counter%2 == 0:
                plot_str += "</div>"
                plot_str += "<div class='row'>"
                gro_str = ""
                gro_str += "<div class='col-lg-6'> <div class='page-header'>"+group+"</div>"
                for img in mice_date[group]:
                    ima_src = ""
                    ima_src += settings.IMAGE_PATH
                    ima_src += img
                    ima_str = ""
                    ima_str += "<div class='col-lg-6 col-lg-4'><img width='350px' height='300px' class='thumbnail img-responsive' src='"+ima_src+"'></a></div>"
                    gro_str += ima_str
                gro_str += "</div>"
                plot_str += gro_str
            else:
                gro_str = ""
                gro_str += "<div class='col-lg-6'> <div class='page-header'>"+group+"</div>"
                for img in mice_date[group]:
                    ima_src = ""
                    ima_src += settings.IMAGE_PATH
                    ima_src += img
                    ima_str = ""
                    ima_str += "<div class='col-lg-6 col-lg-4'><img width='350px' height='300px' class='thumbnail img-responsive' src='"+ima_src+"'></a></div>"
                    gro_str += ima_str
                gro_str += "</div>"
                plot_str += gro_str
            counter += 1
        plot_str += "</div>"
        return plot_str
	
    #case for static
    col = int(col)
    if col > 0:
        width = col*(350*type_number)+250
        width = str(width)
        col_counter = 0
        plot_str = ""+"<table cellpadding='0' cellspacing='0' border='0'> <tr class='row1'>"
        for group in mice_date:
            
            
            if col_counter < col:
                group_str = ""
                group_str += "<td><h1 style='width:150px;left: 0; top: 2'>"+group+"</h1></td>"
                for file_name in mice_date[group]:
                    ima_src = settings.IMAGE_PATH
                    ima_src += file_name
                    #print ima_src
                    group_str += "<td><img  style='width:350px' src='"+ima_src+"' /></td>"
                group_str += "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                plot_str += group_str
                col_counter += 1
            elif col_counter >= col:
                plot_str += "</tr> </table> <br> <hr style='width: "+width+"px' />"
                plot_str += "<table cellpadding='0' cellspacing='0' border='0'> <tr class='row1'>"
                group_str = ""
                group_str += "<td><h1 style='width:150px;left: 0; top: 2'>"+group+"</h1></td>"
                for file_name in mice_date[group]:
                    ima_src = settings.IMAGE_PATH
                    ima_src += file_name
                    #print ima_src
                    group_str += "<td><img  style='width:350px' src='"+ima_src+"' /></td>"
                    #group_str += "<td><img  style='width:350px' src='/static/image/line-chart.png' /></td>"
                group_str += "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>"
                plot_str += group_str                
                col_counter = 1
        plot_str += "</tr> </table> <br> <hr style='width: "+width+"px' />"

    return plot_str
	
#generate the string of URL for sharing.
def link_gene(plo_fil_nam,col):
    link_str = "/link?"
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
    try:
        mice_file = open(settings.SUBJECT_PATH,"r")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    if sub in mice:
        return False
    sub += '\n'
    mice_file.close()
    try:
        mice_file = open(settings.SUBJECT_PATH,"a")
    except:
        print "Can't open the file"
    mice_file.write(sub)
    mice_file.close()
    return True

#function for deleting subject
def del_subject(sub):
    file_path = settings.SUBJECT_PATH
    try:
        mice_file = open(file_path,"r+")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    try:
        mice.remove(sub)
    except:
        return False
    mice_file.close()
    temp_path = file_path+".new"
    temp_file = open(temp_path,'w')
    for mouse in mice:
        mouse += '\n'
        temp_file.write(mouse)
    temp_file.close()
    shutil.move(temp_path, file_path)
    return True
	
#function for wirte profile
def write_profile(mic_lis,plo_lis,dat_ran,col):
    profile = open(settings.SAVE_PROFILE,'a+')
    wri_str = ""
    for mouse in mic_lis:
        mouse = str(mouse) + ','
        wri_str += mouse
    wri_str += ';'
    for plot in plo_lis:
        plot = str(plot) + ','
        wri_str += plot
    wri_str += '\n'
    profile.write(wri_str)
    profile.close()

'''
def reset_pro():
    temp_path = settings.SAVE_PROFILE+".new"
    temp_profile = open(temp_path,'w')
    shutil.move(temp_path,settings.SAVE_PROFILE)
'''

#read profile from file
def read_profile():
    profile = open(settings.SAVE_PROFILE,'r+')
    res_list = []
    pro_list = profile.read().splitlines()
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
    profile_str = ""
    count = 1
    is_break = ""
    for profile in profile_list:
        one_pro_str = ""
        one_pro_str += profile['index']
        one_pro_str += "<br>"
        one_pro_str += str(profile['subject'])
        one_pro_str += "<br>"
        one_pro_str += str(profile['plotType'])
        is_break = "<br>"
        profile_str += "<input type ='checkbox' id='{index1}' name='profile' value='{index2}' class='hidden_profile'>	<label class='' for='{index3}'>	<div class=''>{prof}</div>	</label> {is_bre}".format(index1=str(profile['index']),index2=str(profile['index']),index3=str(profile['index']),prof=one_pro_str,is_bre=is_break)
        count += 1
    return profile_str
	
	
	
# function to delete profile
def dele_profile(index_list):
    str_index_list = []
    for index in index_list:
        str_index_list.append(str(index))
    file_path = settings.SAVE_PROFILE
    try:
        profile = open(file_path,"r+")
    except:
        print "Can't open the file"
    old_pro_lis = profile.read().splitlines()
    profile.close()
	
    new_file_path = file_path+".new"
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
