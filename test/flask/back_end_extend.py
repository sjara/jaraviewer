import datetime
import time
import sys,os

#from jaratoolbox import loadbehavior
import loadbehavior
import settings

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

def get_mice():
    mice = []
	
    try:
        mice_file = open(settings.SUBJECT_PATH,"r")
    except:
        print "Can't open the file"
    mice = mice_file.read().splitlines()
    #print mice
    return mice
	
def format_index(mic):
    mouse_str = ""
    count = 1
    is_break = ""
    for mouse in mic:
        if count%4 == 0:
            is_break = "<br>"
        mouse_str += "<input type ='checkbox' id='subject{count1}' name='subject' value='{subj1}' class='hidden_subject'>	<label class='label_subject btn btn-primary' for='subject{count2}'>	<div class='label_name'>{subj2}</div>	</label> {is_bre}".format(count1=count,subj1=mouse,count2=count,subj2=mouse,is_bre=is_break)
        count += 1
        is_break = ""
    #print mouse_str
    return mouse_str

def date_generator(raw_date_str):
    star_year = int(raw_date_str[START_YEAR_STA:START_YEAR_END])
    star_month = int(raw_date_str[START_MONTH_STA:START_MONTH_END])
    star_day = int(raw_date_str[START_DAY_STA:START_DAY_END])
    end_year = int(raw_date_str[END_YEAR_STA:END_YEAR_END])
    end_month = int(raw_date_str[END_MONTH_STA:END_MONTH_END])
    end_day = int(raw_date_str[END_DAY_STA:END_DAY_END])
    start_date = datetime.date(star_year,star_month,star_day)
    end_date = datetime.date(end_year,end_month,end_day)
    #print "{start_date}, {end_date}".format(start_date=str(start_date),end_date=str(start_date))
    
    date_list = []
    temp_date = start_date
    delta = end_date - start_date
    delta = int(delta.days)
    for i in range(0,delta+1):
        #print temp_date
        date_str = temp_date.strftime("%Y%m%d")
        date_str = date_str + 'a'
        #print date_str
        date_list.append(date_str)
        temp_date += datetime.timedelta(days=1)
        #print
    #print date_list
    return date_list
	
	
def get_plot(mice,date,plo_typ):

    EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
    paradigm = '2afc'

    subject_list = mice
    session_list = date
    #session = '20160310a' # This is the date formatted as YYYYMMDD and one more character (usually 'a')

	
    all_file_name = []
    #non_exsi_file = []
    for subject in subject_list:
        for session in session_list:
            behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
            behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
            #print str(subject),str(session),"!!!!!!!!!!!!!!!!!!!!!"
            for plot_type in plo_typ:
                out_dict = form_out_put(sub=subject,typ=plot_type,data=behavData,sess=session)
                all_file_name.append(out_dict['filename'])
                #print str(check_exsit(fil_nam=out_dict['filename'])),out_dict['filename']
                if not check_exsit(fil_nam=out_dict['filename']):
                    #non_exsi_file.append(out_dict['filename'])
                    #plot_function(out_dict)
                    #test_plot(out_dic=out_dict)
                    print
					
    
    #print non_exsi_file
    #print all_file_name
                #plot_function()
            #behav_list.append(behavData)
    
	# -- Find the data filename and load the data into a data object (similar to a Python dict) --
    #behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)

    #behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

    #print behav_list

    return all_file_name

#get_data(data_arra=numpy.array(['adap021']))


def form_out_put(sub,typ,data,sess):
    out_dict = {}
    #print str(sub),"sub",str(typ),"typ",sess,"sess"
    out_dict['type'] = str(typ)
    #print sess
    form_sess = sess[0:-1]
    #print form_sess
    out_dict['filename'] = str(sub)+'_'+str(form_sess)+'_'+str(typ)+'.svg'
    #print out_dict['filename']
    out_dict['data'] = data
    return out_dict
	
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

def plot_render(plo_fil_nam,col):
    mice_date = {}
    for plot in plo_fil_nam:
        stri = plot.split('_',3)
        mice_date_str = stri[0]+'-'+stri[1]
        if mice_date_str in mice_date.keys():
            mice_date[mice_date_str].append(plot)
        else:
            mice_date[mice_date_str] = []
            mice_date[mice_date_str].append(plot)
        #print mouse
        #print date
    #print mice_date
	
    width = 12/int(col)
    plot_str = ""
    for group in mice_date:
        mouse_str = '''
					<div class="row">
						<div class="col-lg-12">
							<h1 class="page-header">{gro}</h1>
						</div>
						<!-- /.col-lg-12 -->
					</div>
					<!-- /.row -->
					<div class="row">
					'''.format(gro=group)
        panel_str = ""
        for file_name in mice_date[group]:
            #print file_name
            image_path = "/static/image/"+file_name
            #print image_path
            image_str = "<div class='col-lg-{wid}'>	<div class='panel panel-default'><div class='panel-heading'>{fil_nam}</div>	<div class='panel-body'><div class=panel-image>".format(fil_nam=file_name,wid=width)
            image_str += "<img src='{ima_pat}' class='img-responsive center-block'>".format(ima_pat=image_path)
            image_str += "</div></div></div></div>"
            panel_str += image_str
            print image_str
        temp_str = mouse_str+panel_str+"</div>"
        plot_str += temp_str
	
    #print plot_str
    #print mice_name
    #print date_list
        #mice_str += mouse_str	
    #return mice_str
    return plot_str
	

def link_gene(plo_fil_nam,col):
    #link_str = settings.URL_LINK
    link_str = "/link?"
    count = 0
    for plot_name in plo_fil_nam:
        temp_str = "plot"+str(count)+"="+plot_name+'&'
        link_str += temp_str
        count +=1
    link_str += "num="+str(count)
    link_str += "&col=" + str(col)
    print link_str
    return link_str
