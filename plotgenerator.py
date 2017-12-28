'''
Module for generating and saving data plots.
This version relies on jaratoolbox for making the plots.
'''

import numpy as np
import matplotlib
matplotlib.use('Agg') # Set no graphical backend
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
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


def info_text(behavData,fontsize=12):
    '''
    Show summary of session.
    First argument is an object created by jaratoolbox.loadbehavior.BehaviorData (or subclasses)
    '''

    '''
    #possibleFreq = np.unique(behavData['targetFrequency'])
    if soundfreq is None:
        possibleFreq = np.unique(behavData['targetFrequency'])
    else:
        possibleFreq = soundfreq
    possibleBlockID = np.unique(behavData['currentBlock'])
    trialsEachType = find_trials_each_type_each_block(behavData['targetFrequency'],possibleFreq,
                                                      behavData['currentBlock'],possibleBlockID)
    validTrialsEachType = trialsEachType & behavData['valid'][:,np.newaxis,np.newaxis].astype(bool)
    correctTrialsEachType = validTrialsEachType & correct[:,np.newaxis,np.newaxis]
    nCorrectEachType = np.sum(correctTrialsEachType,axis=0)
    nValidEachType = np.sum(validTrialsEachType,axis=0)

    #perfEachType = np.where(nValidEachType>0, nCorrectEachType/nValidEachType.astype(float), np.nan)
    perfEachType = nCorrectEachType/nValidEachType.astype(float)

    # --- Plot results ---
    itemsToPlot = nValidEachType.flatten()>0  #~np.isnan(perfEachType.flatten())
    perfToPlot = perfEachType.flatten()[itemsToPlot] # Show only 2 freq for each block type
    freqLabels = np.repeat(possibleFreq,len(possibleBlockID))[itemsToPlot]
    nValidCounts = nValidEachType.flatten()[itemsToPlot]
    xPos = [0,1,3,4][:len(perfToPlot)]
    ax = plt.gca()
    ax.set_xlim([-1,5])
    ax.set_ylim([0,100])
    plt.hold(True)
    hline50 = plt.axhline(50,linestyle=':',color='k',zorder=-1)
    hline75 = plt.axhline(75,linestyle=':',color='k',zorder=-1)
    hbars = plt.bar(xPos,100*perfToPlot,align='center',fc=[0.8,0.8,0.8],ec='k')
    for thispos,thistext in zip(xPos,nValidCounts):
        plt.text(thispos,10,str(thistext),ha='center',fontsize=fontsize)
    ax.set_ylabel('% correct',fontsize=fontsize)
    ax.set_xticks(xPos)
    ax.set_xticklabels(freqLabels/1000)
    '''
    correct = behavData['outcome']==behavData.labels['outcome']['correct']
    early = behavData['outcome']==behavData.labels['outcome']['invalid']
    noChoice = behavData['outcome']==behavData.labels['outcome']['nochoice']
    nTrials = len(early)
    valid = np.sum(~(early|noChoice))
    fractionEarly = np.sum(early)/float(nTrials)
    fractionCorrect = np.sum(correct)/float(np.sum(valid))
    stringValid = '{} valid'.format(valid)
    stringTotal = '{} total'.format(nTrials)
    stringEarly = '{:0.0%} early'.format(fractionEarly)
    stringCorrect = '{:0.0%} correct'.format(fractionCorrect)
    ax = plt.gca()
    stringsToShow = [behavData.session['subject'],
                     behavData.session['date'][:10], behavData.session['date'][11:],
                     behavData.session['hostname'], '', stringValid, stringCorrect, '', stringEarly]
    vOffset = 1
    ax.hold(True)
    for inds,oneString in enumerate(stringsToShow):
        #oneLabel = plt.text(0, -inds*vOffset, oneString, fontsize=fontsize, fontweight='bold')
        oneLabel = plt.text(0, -inds*vOffset, oneString, fontsize=fontsize, fontweight='normal')
        #print('================ x ==============')
        if inds==0:
            oneLabel.set_fontweight('bold')
    ax.set_ylim([-10,1])
    ax.set_axis_off()
    #titleStr = '{0} [{1}] {2}\n'.format(behavData.session['subject'],behavData.session['date'],
    #                                    behavData.session['hostname'])
    #ax.set_title(titleStr,fontweight='bold',fontsize=fontsize,y=0.95)
    '''
    titleStr += '{0} valid, {1:.0%} early'.format(sum(nValidCounts),np.mean(early))
    ax.set_title(titleStr,fontweight='bold',fontsize=fontsize,y=0.95)
    ax.set_xlabel('Frequency (kHz)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(ax,fontsize)
    '''

