from jaratoolbox import loadbehavior
from jaratoolbox import settings
import plotgenerator 
import time
def Test():
    #Test function: Used to test code from plotgenerator 
    # NOTE: this text function will be a mini version of what the backend will be doing each time
    #code from "test032_example_read_bdata.py" by Santiago Jaramillo
    EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
    paradigm = '2afc'
    subject = 'adap021'
    session = '20160310a' # This is the date formatted as YYYYMMDD and one more character (usually 'a')

    # -- Find the data filename and load the data into a data object (similar to a Python dict) --
    behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
    behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')
    #end Santiago's code
    #make each dictionary (for test, 1 per graph type) and append them to the list
    graphList = []
    '''
    #Test 1: Simple one of each graph test
    
    graphDict1 = {'type' : "psychometric", 'filename' : "adap021_20160310_psychometric.svg", 'data' : behavData}
    graphList.append(graphDict1)
    graphDict2 = {'type' : "summary", 'filename' : "adap021_20160310_summary.svg", 'data' : behavData}
    graphList.append(graphDict2)
    graphDict3 = {'type' : "dynamics", 'filename' : "adap021_20160310_dynamics.svg", 'data' : behavData}
    graphList.append(graphDict3)
    '''
    #'''
    #Test2: stress test. 20 summary, 20 dynamics
    graphDictPsy = {'type' : "psychometric", 'filename' : "adap021_20160310_psychometric.svg", 'data' : behavData}
    graphDictDyn = {'type' : "dynamics", 'filename' : "adap021_20160310_dynamics.svg", 'data' : behavData}
    for i in range(20):
        graphList.append(graphDictPsy)
        graphList.append(graphDictDyn)
    #'''
    #time.time returns the current system time in seconds. by taking the time before and after running the Generate function and taking the difference,
    #we can see the exact time in seconds that the module took to run.
    t0 = time.time()
    Generate(graphList)
    t1 = time.time()
    print(t1-t0)