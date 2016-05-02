#!/usr/bin/env python

import os
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis

from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

class Alarm(object):
    # TODO: This should most likely be running constantly, or whenever new data is availible to check. 

    def __init__(self, threshold):
        # A basic threshold, to detect if average performance falls below it. 
        self.behavData      = [] 
        self.threshold      = threshold

    def loadData(self):
        for info in os.walk(settings.BEHAVIOR_PATH):
            path = info[0]

            for element in info[2]:
                name, extension = element.split(".")
                if(extension == "h5"):
                    full_path = os.path.join(path, element)
                    self.behavData.append((name, loadbehavior.FlexCategBehaviorData(full_path, readmode='full')))

    def alert(self, sender, destination, password):
        # TODO: Multiple types of alerts (e.g. No data for a certain animal, average below and above a certain threshold, etc.)
        # TODO: Probably shouldn't be storing the user/password in plaintext

        for name, data in self.behavData:
            if(self.calculateAverage(data) < self.threshold):

                print("Average below acceptable amount for " + name + ". Sending alert.")

                """
                To test the email sending capability, replace "username@uoregon.edu" with a testing username, 
                and the corresponding password below, before uncommenting.

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

    def calculateAverage(self, data):
        nValidTrials        = data['nValid'][-1]
        nRewardTrials       = data['nRewarded'][-1]
        return float(nRewardTrials)/nValidTrials

def main():
    # Set the threshold so high it will always alert (for testing purposes)
    alarm = Alarm(1)
    alarm.loadData()
    alarm.alert("username@uoregon.edu", "username@uoregon.edu", "password") 

if __name__ == "__main__":
    main()
