import loadbehavior
import settings
#import numpy

def get_data(data_arra):

    EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
    paradigm = '2afc'

    subject = data_arra[0]
    session = '20160310a' # This is the date formatted as YYYYMMDD and one more character (usually 'a')

	# -- Find the data filename and load the data into a data object (similar to a Python dict) --
    behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)

    behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

    #print behavData

    return behavData

#get_data(data_arra=numpy.array(['adap021']))
