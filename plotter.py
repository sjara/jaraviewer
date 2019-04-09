'''
Module for generating and saving data plots.
Ideally, plot functions are defined in jaratoolbox and just called from here.

To add a new plot you need:
1. Create or define what icon to use from .../static/icons/ (e.g., psychometrics.svg)
2. Add a key to the ordered dict PLOTS below, and specify label and icon.
3. Create a plotting function at the end of this script using the same name as the new key.
   The plotting function should be minimal (most code should be in jaratoolbox).

'''

import numpy as np
import matplotlib
from collections import OrderedDict
matplotlib.use('Agg') # Set no graphical backend
import matplotlib.pyplot as plt
from jaratoolbox import behavioranalysis
import os

FONTSIZE = 20

PLOTS = OrderedDict()
PLOTS.update({'info'        :{'label':'Info', 'icon':'info.svg'}})
PLOTS.update({'summary'     :{'label':'Summary', 'icon':'summary.svg'}})
#PLOTS.update({'psychometric':{'label':'Psychometric', 'icon':'psychometric.svg'}})
PLOTS.update({'psycurveLog'  :{'label':'Psycurve (log)', 'icon':'psychometric.svg'}})
PLOTS.update({'psycurveLinear':{'label':'Psycurve (linear)', 'icon':'psychometric.svg'}})
PLOTS.update({'dynamics'    :{'label':'Dynamics', 'icon':'dynamics.svg'}})


def generate(bdata, plottype, outputpath, filename):
    '''
    bdata   : behavior data (loaded by jaratoolbox.loadbehavior)
    plottype: (string) Type of plot from the list defined above in PLOTS.
    outputpath: (string) Path to save files to (usually comes from settings file)
    filename: (string) Output filename.
    '''
    plt.clf()
    if plottype in PLOTS:
        plotfun = globals()[plottype]
        plotfun(bdata)
    else:
        raise ValueError('Plot type {0} is not valid'.format(plottype))
    outputFile = os.path.join(outputpath, filename)
    print 'Saving plot to {0}'.format(outputFile)
    plt.savefig(outputFile)


# ======= Plot function should be defined below ========

#def psychometric(bdata):
#    behavioranalysis.plot_frequency_psycurve(bdata,fontsize=FONTSIZE)
#    plt.gcf().set_size_inches([8,6])

def psycurveLog(bdata):
    behavioranalysis.plot_frequency_psycurve(bdata,fontsize=FONTSIZE)
    plt.gcf().set_size_inches([8,6])

def psycurveLinear(bdata):
    from jaratoolbox import extraplots
    fontsize=FONTSIZE
    if 'targetPercentage' in bdata.viewkeys():
        targetPercentage = bdata['targetPercentage']
    else:
        targetPercentage = bdata['targetFrequency'] # I used name 'frequency' initially
    choiceRight = bdata['choice']==bdata.labels['choice']['right']
    valid=bdata['valid']& (bdata['choice']!=bdata.labels['choice']['none'])
    (possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue)=\
           behavioranalysis.calculate_psychometric(choiceRight,targetPercentage,valid)
    (pline, pcaps, pbars, pdots) = extraplots.plot_psychometric(1e-3*possibleValues,fractionHitsEachValue,
                                                                    ciHitsEachValue,xTickPeriod=1, xscale='linear')
    plt.xlabel('Stimulus',fontsize=fontsize)
    plt.ylabel('Rightward trials (%)',fontsize=fontsize)
    extraplots.set_ticks_fontsize(plt.gca(),fontsize)
    plt.gcf().set_size_inches([8,6])

def summary(bdata):    
    freqsToUse = [bdata['lowFreq'][-1],bdata['highFreq'][-1]]
    behavioranalysis.plot_summary(bdata,fontsize=FONTSIZE,soundfreq=freqsToUse)
    plt.gcf().set_size_inches([8,6])

def dynamics(bdata):
    freqsToUse = [bdata['lowFreq'][-1],bdata['highFreq'][-1]]
    hPlots = behavioranalysis.plot_dynamics(bdata,winsize=40,fontsize=FONTSIZE,soundfreq=freqsToUse)
    plt.gca().set_xlim([0,1000])
    plt.setp(hPlots,lw=4)
    plt.gcf().set_size_inches([8,6])
    
def info(bdata,fontsize=FONTSIZE):
    '''
    Show summary of session.
    First argument is an object created by jaratoolbox.loadbehavior.BehaviorData (or subclasses)
    '''
    correct = bdata['outcome']==bdata.labels['outcome']['correct']
    early = bdata['outcome']==bdata.labels['outcome']['invalid']
    noChoice = bdata['outcome']==bdata.labels['outcome']['nochoice']
    nTrials = len(early)
    valid = np.sum(~(early|noChoice))
    fractionEarly = np.sum(early)/float(nTrials)
    fractionCorrect = np.sum(correct)/float(np.sum(valid))
    stringValid = '{} valid'.format(valid)
    stringTotal = '{} total'.format(nTrials)
    stringEarly = '{:0.0%} early'.format(fractionEarly)
    stringCorrect = '{:0.0%} correct'.format(fractionCorrect)
    ax = plt.gca()
    stringsToShow = [bdata.session['subject'],
                     bdata.session['date'][:10], bdata.session['date'][11:],
                     bdata.session['hostname'], '', stringValid, stringCorrect, '', stringEarly]
    vOffset = 1
    ax.hold(True)
    for inds,oneString in enumerate(stringsToShow):
        oneLabel = plt.text(0, -inds*vOffset, oneString, fontsize=fontsize, fontweight='normal')
        if inds==0:
            oneLabel.set_fontweight('bold')
    ax.set_ylim([-10,1])
    ax.set_axis_off()
    plt.gcf().set_size_inches([2,6])

