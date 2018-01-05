'''
Module for generating and saving data plots.
This version relies on jaratoolbox for making the plots.
'''

import numpy as np
import matplotlib
matplotlib.use('Agg') # Set no graphical backend
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
from .plugins import coreplots
import os

FONTSIZE = 20

def generate(plotInfo, outputpath):
    '''
    FIXME: finish this docstring

    plotList should be a list of dictionaries, each dictionary with the following parameters:
    'type': (string) Type of plot. Accepted values are 'psychometric', 'summary', or 'dynamics' 
    'filename': (string) Output file name.
    THIS IS NOT NECESSARY, THIS METHOD SHOULD NOT CARE: using format "mousename_YYYYMMDD_plotType.svg"
    'data': raw behavior data created by jaratoolbox.loadbehavior.FlexCategBehaviorData()

    Files are saved to settings.IMAGE_PATH
    '''
    plt.clf()
    plotData = plotInfo['data']
    if plotInfo['type'] == 'psychometric':
        #behavioranalysis.plot_frequency_psycurve(plotData,fontsize=FONTSIZE)
        #plt.gcf().set_size_inches([8,6])
        coreplots.psychometric(plotData)
    elif plotInfo['type'] == 'info':
        #info_text(plotData,fontsize=FONTSIZE)
        #plt.gcf().set_size_inches([2,6])
        coreplots.infotext(plotData)
    elif plotInfo['type'] == 'summary':
        #freqsToUse = [plotData['lowFreq'][-1],plotData['highFreq'][-1]]
        #behavioranalysis.plot_summary(plotData,fontsize=FONTSIZE,soundfreq=freqsToUse)
        #plt.gcf().set_size_inches([8,6])
        coreplots.summary(plotData)
    elif plotInfo['type'] == 'dynamics':
        #freqsToUse = [plotData['lowFreq'][-1],plotData['highFreq'][-1]]
        #hPlots = behavioranalysis.plot_dynamics(plotData,winsize=40,fontsize=FONTSIZE,soundfreq=freqsToUse)
        #plt.gca().set_xlim([0,1000])
        #plt.setp(hPlots,lw=4)
        #plt.gcf().set_size_inches([8,6])
        coreplots.dynamics(plotData)
    else:
        raise ValueError('Plot type {0} is not valid'.format(plotInfo['type']))
    outputFile = os.path.join(outputpath, plotInfo['filename'])
    print 'Saving plot to {0}'.format(outputFile)
    plt.savefig(outputFile)
    #plt.close()


def old_generate(plotInfo, outputpath):
    '''
    FIXME: finish this docstring

    plotList should be a list of dictionaries, each dictionary with the following parameters:
    'type': (string) Type of plot. Accepted values are 'psychometric', 'summary', or 'dynamics' 
    'filename': (string) Output file name.
    THIS IS NOT NECESSARY, THIS METHOD SHOULD NOT CARE: using format "mousename_YYYYMMDD_plotType.svg"
    'data': raw behavior data created by jaratoolbox.loadbehavior.FlexCategBehaviorData()

    Files are saved to settings.IMAGE_PATH
    '''
    plt.clf()
    plotData = plotInfo['data']
    if plotInfo['type'] == 'psychometric':
        behavioranalysis.plot_frequency_psycurve(plotData,fontsize=FONTSIZE)
        plt.gcf().set_size_inches([8,6])
    elif plotInfo['type'] == 'infoText':
        info_text(plotData,fontsize=FONTSIZE)
        plt.gcf().set_size_inches([2,6])
    elif plotInfo['type'] == 'summary':
        freqsToUse = [plotData['lowFreq'][-1],plotData['highFreq'][-1]]
        behavioranalysis.plot_summary(plotData,fontsize=FONTSIZE,soundfreq=freqsToUse)
        plt.gcf().set_size_inches([8,6])
    elif plotInfo['type'] == 'dynamics':
        freqsToUse = [plotData['lowFreq'][-1],plotData['highFreq'][-1]]
        hPlots = behavioranalysis.plot_dynamics(plotData,winsize=40,fontsize=FONTSIZE,soundfreq=freqsToUse)
        plt.gca().set_xlim([0,1000])
        plt.setp(hPlots,lw=4)
        plt.gcf().set_size_inches([8,6])
    else:
        raise ValueError('Plot type {0} is not valid'.format(plotInfo['Type']))
    outputFile = os.path.join(outputpath, plotInfo['filename'])
    print 'Saving plot to {0}'.format(outputFile)
    plt.savefig(outputFile)
    #plt.close()

