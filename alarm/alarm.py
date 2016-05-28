#!/usr/bin/env python
import os
import alarm_settings
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extrafuncs

from datetime import date
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

class Alarm(object):
    def __init__(self, threshold = 0, subjects = [], subscribers = [], belowThreshold = False, aboveThreshold = False, missingData = False):
        self.behavData      = [] 

        # Flags for certain alarms
        self.threshold      = threshold
        self.belowThreshold = belowThreshold
        self.aboveThreshold = aboveThreshold
        self.missingData    = missingData
        self.subjects       = subjects
        self.subscribers    = subscribers

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
                split           = element.split(".")

                if(len(split) == 2):
                    name, extension = element.split(".")

                    for animal in self.subjects:
                        experimentDate  = name.split("_")[-1]
                        isoDate         = experimentDate[:4] + "-" + experimentDate[4:6] + "-" + experimentDate[6:8]
                        today           = date.today() 

                        # We only want data from today from an animal that we care about
                        if(extension == "h5" and animal in name):
                            try:
                                full_path = os.path.join(path, element)
                                self.behavData.append((full_path, loadbehavior.BehaviorData(full_path, readmode='full')))
                            except:
                                self.sendToAllSubscribers("Error when attempting to load " + full_path + ".", "Alert: Alarm error")

    def parseFilePath(self, filepath):
        li                      = filepath.split("/") 
        last                    = li[-1].split("_")

        self.subjectName        = li[-2]
        self.experimenterName   = li[-3]
        self.experimentDate     = last[-1]
        self.paradigm           = last[-2]
        self.subjectName        = last[-3]

    def sendToAllSubscribers(self, message, subject):
        for destination in self.subscribers:
            self.sendEmail(destination, message, subject)

    def sendEmail(self, destination, message, subject):
        smtpServer          = "smtp.uoregon.edu"
        textSubtype         = "plain"

        f                   = open(alarm_settings.path_to_auth)
        text                = f.read()
        sender, password    = text.split()

        # Setup message variables 
        msg             = MIMEText(message)
        msg['Subject']  = subject
        msg['From']     = sender

        # Setup the connection, and attempt to send the message.
        print("To: " + destination)
        print("From: " + sender)
        print("Subject: " + subject)
        print("Body: " + message + "\n")

        """
        conn            = SMTP(smtpServer)
        conn.set_debuglevel(False)
        conn.login(sender, password)
        conn.sendmail(sender, destination, msg.as_string())
        conn.close()
        """

    def belowThresholdAlarm(self, data):
         if(self.calculateAverage(data) < self.threshold and self.belowThreshold):
                    message = "Average below acceptable amount for " + self.subjectName + "."
                    self.sendToAllSubscribers(message, "Alert: Average performance below threshold.")

    def aboveThresholdAlarm(self, data):
        if(self.calculateAverage(data) > self.threshold and self.aboveThreshold):
                message = "Average above acceptable amount for " + self.subjectName + "."
                self.sendToAllSubscribers(message, "Alert: Average performance above threshold.")

    def isMissingDataAlarm(self):
        if(self.missingData and len(self.subjects) != 0):
            for animal in self.subjects:
                self.sendToAllSubscribers("Missing data for " + animal + ".", "Alert: Missing data")

    def alert(self):
        self.loadData()

        for path, data in self.behavData:
            self.parseFilePath(path)
            if self.subjectName in self.subjects:
                self.subjects.remove(self.subjectName)

                self.belowThresholdAlarm(data)
                self.aboveThresholdAlarm(data)

        self.isMissingDataAlarm()
        
    def calculateAverage(self, data):
        nValidTrials        = data['nValid'][-1]
        nRewardTrials       = data['nRewarded'][-1]
        return float(nRewardTrials)/nValidTrials
