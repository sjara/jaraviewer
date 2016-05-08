import datetime
import time

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

def date_generator(raw_date_str):
    #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
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
        #date_str = temp_date.strftime("%d")
        #print date_str+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        date_str = temp_date.strftime("%Y%m%d")
        date_str = date_str + 'a'
        #print date_str
        date_list.append(date_str)
        temp_date += datetime.timedelta(days=1)
        #print
    #print date_list
    return date_list
	
	
def get_data(mice,date):

    EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
    paradigm = '2afc'

    subject_list = mice
    session_list = date
    #session = '20160310a' # This is the date formatted as YYYYMMDD and one more character (usually 'a')

	
    behav_list = []
    for subject in subject_list:
        for session in session_list:
            behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
            behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
            behav_list.append(behavData)
    
	# -- Find the data filename and load the data into a data object (similar to a Python dict) --
    #behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)

    #behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

    #print behav_list

    return behav_list

#get_data(data_arra=numpy.array(['adap021']))
