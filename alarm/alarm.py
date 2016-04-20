#!/usr/bin/env python

from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

class Alarm(object):
    # TODO: This should most likely be running constantly, or whenever new data is availible to check. 

    def __init__(self, experimenter, paradigm, subject, session, threshold):

        # Setup the file and the data
        # FIXME: We really shouldn't be hardcoding any of this. We should be scanning through the directories, checking each one.
        self.experimenter   = experimenter
        self.paradigm       = paradigm
        self.subject        = subject
        self.session        = session
        self.behavFile      = loadbehavior.path_to_behavior_data(subject,experimenter,paradigm,session)
        self.behavData      = loadbehavior.FlexCategBehaviorData(self.behavFile, readmode='full')

        # A basic threshold, to detect if average performance falls below it. 
        self.threshold      = threshold

    def alert(self, sender, destination, password):
        # TODO: Multiple types of alerts (e.g. No data for a certain animal, average below and above a certain threshold, etc.)
        # TODO: Actually scan through each animal's daily reports, rather than just going off the hardcoded test data.

        if(self.calculateAverage() < self.threshold):

            print("Average below acceptable amount. Sending alert.")

            smtpServer      = "smtp.uoregon.edu"
            textSubtype     = "plain"

            # Setup message variables 
            msg             = MIMEText("This is a test alert.")
            msg['Subject']  = "Alarm alert: Performance below threshold"
            msg['From']     = sender 

            # Setup the connection, and attempt to send the message.
            conn            = SMTP(smtpServer)
            conn.set_debuglevel(False)
            conn.login(sender, password)
            conn.sendmail(sender, destination, msg.as_string())
            conn.close()


    def calculateAverage(self):
        nValidTrials        = self.behavData['nValid'][-1]
        nRewardTrials       = self.behavData['nRewarded'][-1]
        return float(nRewardTrials)/nValidTrials

def main():
    # Set the threshold so high it will always alert (for testing purposes)
    alarm = Alarm(settings.DEFAULT_EXPERIMENTER, '2afc', 'adap021', '20160310a', 1)

    # To test the email sending capability, replace "username@uoregon.edu" with a testing username, and the corresponding password, before
    # uncommenting.
    # alarm.alert("username@uoregon.edu", "username@uoregon.edu", "password") 

if __name__ == "__main__":
    main()
