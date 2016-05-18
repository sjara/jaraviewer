#Plot generation code for the Jaraviewer web framework
#By: James Vargas-Witherell
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
import settings
'''
INPUT CONVENTIONS:
plotList should be a list of dictionaries, each dictionary with the following parameters:
'type' : Contains the requested type of plot as a string. Accepted values are "psychometric", "summary", or "dynamics" 
'filename' : Contains the filename as the string. The filename should be in the format "mousename_YYYYMMDD_plotType.svg"
'data': Contains the raw data gained from the loadbehavior.FlexCategBehaviorData(behavFile,readmode='full') function in jaratoolbox

A parameter may be added that contains the filepath to the graph storage folder. Need to discuss
'''
#Path variable. Currently is an empty string, so files will be stored in the current directory
path = settings.IMAGE_PATH
def Generate(plotList):
#plotList is the list of plot dictionaries as specified above
    for plot in plotList:
        #get the data from the dictionary
        plotData = plot['data']
        #check what the plot type is and run the coorisponding method
        #basis for method calls taken from "test032_example_read_bdata.py" by Santiago Jaramillo
        if plot['type'] is "psychometric":
            #As mentioned by Santiago: parameters returned from psychometric plot are not used. Were put in place for improvments that were never finished
            (pline, pcaps, pbars, pdots) = behavioranalysis.plot_frequency_psycurve(plotData,fontsize=14)
        elif plot['type'] is "summary":
            freqsToUse = [plotData['lowFreq'][-1],plotData['highFreq'][-1]]
            behavioranalysis.plot_summary(plotData,fontsize=14,soundfreq=freqsToUse)
        elif plot['type'] is "dynamics":
            freqsToUse = [plotData['lowFreq'][-1],plotData['highFreq'][-1]]
            behavioranalysis.plot_dynamics(plotData,winsize=40,fontsize=14,soundfreq=freqsToUse)
        else:
            #ERROR case: plot type invalid
            return False
        #save the plot under the given filepath
        plt.savefig(os.path.join(path, plot['filename']))
    return True 



