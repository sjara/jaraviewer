#!/usr/bin/env python

import os
import alarm_settings
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

class Alarm(object):
    # TODO: This should most likely be running constantly, or whenever new data is availible to check. 

    def __init__(self, threshold = 0, belowThreshold = False, aboveThreshold = False, missingData = False):
        # A basic threshold, to detect if average performance falls below it. 
        self.behavData      = [] 

        # Flags for certain alarms
        self.threshold      = threshold
        self.belowThreshold = belowThreshold
        self.aboveThreshold = aboveThreshold
        self.missingData    = missingData

        # Information from parsed filepath
        self.subjectName        = None
        self.experimentData     = None
        self.paradigm           = None
        self.experimenterName   = None
        self.experimentDate     = None

    def loadData(self):
        # Load all the data availible into a list for later processing.

        for info in os.walk(settings.BEHAVIOR_PATH):
            path = info[0]

            for element in info[2]:
                name, extension = element.split(".")
                if(extension == "h5"):
                    full_path = os.path.join(path, element)
                    self.behavData.append((full_path, loadbehavior.FlexCategBehaviorData(full_path, readmode='full')))

    def parseFilePath(self, filepath):
        li                      = filepath.split("/") 
        last                    = li[-1].split("_")

        self.subjectName        = li[-2]
        self.experimenterName   = li[-3]
        self.experimentDate     = last[-1]
        self.paradigm           = last[-2]
        self.subjectName        = last[-3]

    def alert(self):
        # TODO: Probably shouldn't be storing the user/password in plaintext

        for path, data in self.behavData:
            self.parseFilePath(path)
            if(self.calculateAverage(data) < self.threshold and self.belowThreshold):

                print("Average below acceptable amount for " + self.subjectName + ". Sending alert to " + 
                        self.experimenterName +  " using " + alarm_settings.contact_dict[self.experimenterName][0] + ".")

                """
                To test the email sending capability, replace "username@uoregon.edu" with a testing username, 
                and the corresponding password below, before uncommenting.

                sender          = alarm_settings.contact_dict["test"][0]
                destination     = alarm_settings.contact_dict[self.experimenterName][0]

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
                """

            if(self.calculateAverage(data) > self.threshold and self.aboveThreshold):
                print("Average above acceptable amount for " + self.subjectName + ". Sending alert to " + 
                        self.experimenterName +  " using " + alarm_settings.contact_dict[self.experimenterName][0] + ".")

            if(self.missingData):
                # TODO
                pass

    def calculateAverage(self, data):
        nValidTrials        = data['nValid'][-1]
        nRewardTrials       = data['nRewarded'][-1]
        return float(nRewardTrials)/nValidTrials

def main():
    # Set the threshold so high it will always alert (for testing purposes)
    alarm = Alarm(threshold = 1, belowThreshold = True)
    alarm.loadData()
    alarm.alert()

if __name__ == "__main__":
    main()
