import settings
import loadbehavior
import behavioranalysis
import matplotlib.pyplot as plt
import ArraData as ad

EXPERIMENTER = settings.DEFAULT_EXPERIMENTER
paradigm = '2afc'

subject = 'adap021'
session = '20160310a' # This is the date formatted as YYYYMMDD and one more character (usually 'a')

# -- Find the data filename and load the data into a data object (similar to a Python dict) --
behavFile = loadbehavior.path_to_behavior_data(subject,EXPERIMENTER,paradigm,session)
behavData = loadbehavior.FlexCategBehaviorData(behavFile,readmode='full')

# -- Calculate average performance --
nValidTrials = behavData['nValid'][-1]
nRewardedTrials = behavData['nRewarded'][-1]
#print 'Average performance: {:0.1%}'.format(float(nRewardedTrials)/nValidTrials)

# -- Plot psychometric curve --
(pline, pcaps, pbars, pdots) = behavioranalysis.plot_frequency_psycurve(behavData,fontsize=14)
#plt.show()

'''
# arrange process
# prepare to arrange the data
arraydata = ad.ArraData(behavData)
arraydata.set_name(subject)
arraydata.set_session(session)
arraydata.set_paradigm(paradigm)

# single subject in the array
print arraydata.arrange_data('psychometric')
print arraydata.get_array()
print "--------------------------------------"
print arraydata.arrange_data('summary')
print arraydata.get_array()
print "--------------------------------------"
print arraydata.arrange_data('dynamics')
print arraydata.get_array()
print "--------------------------------------"
print arraydata.arrange_data('dsadsadsa')
print arraydata.get_array()
print "\n--------------------------------------"
# prepare to arrange the data
arraydata.switch_data(behavData) # renew data source
arraydata.set_name(subject)
arraydata.set_session(session)
arraydata.set_paradigm(paradigm)

# multiple subject in the array
print arraydata.arrange_data('psychometric')
print arraydata.arrange_data('summary')
print arraydata.arrange_data('dynamics')
print arraydata.get_array()
'''

print "left choice: \n{lc} \ntype:{type}".format(lc=behavData.labels['choice'],type=type(behavData.labels['choice']))

print "subject={s}\ndate={d}\nhostname={h}".format(s=behavData.session['subject'],d=behavData.session['date'],
                                                    h=behavData.session['hostname'])
													
print behavData.session

(possibleValues,fractionHitsEachValue,ciHitsEachValue,nTrialsEachValue,nHitsEachValue) = behavioranalysis.calculate_psychometric(behavData['choice']
,behavData['targetFrequency'],behavData['valid'])

#print "possibleValues: \n{p}".format(p=possibleValues)
#print "fractionHitsEachValue: \n{f}".format(f=fractionHitsEachValue)
#print "ciHitsEachValue: \n{c}".format(c=ciHitsEachValue)

######try to build a analyze data list###########
pltDict1 = {'type':'psychometric','title':'My plot','possibleValues':possibleValues,
'fractionHitsEachValue':fractionHitsEachValue,'ciHitsEachValue':ciHitsEachValue}
plotList = [pltDict1]
print plotList[0]
