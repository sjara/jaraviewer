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

    def loadData(self, animals):
        # Load all the data availible into a list for later processing.

        for info in os.walk(settings.BEHAVIOR_PATH):
            path = info[0]

            for element in info[2]:
                name, extension = element.split(".")

                for animal in animals:
                    experimentDate  = name.split("_")[-1]
                    isoDate         = experimentDate[:4] + "-" + experimentDate[4:6] + "-" + experimentDate[6:8]
                    today           = date.today() 

                    if(today == extrafuncs.parse_isodate(isoDate) and extension == "h5" and animal in name):
                        full_path = os.path.join(path, element)
                        self.behavData.append((full_path, loadbehavior.BehaviorData(full_path, readmode='full')))

    def parseFilePath(self, filepath):
        li                      = filepath.split("/") 
        last                    = li[-1].split("_")

        self.subjectName        = li[-2]
        self.experimenterName   = li[-3]
        self.experimentDate     = last[-1]
        self.paradigm           = last[-2]
        self.subjectName        = last[-3]

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

    def belowThresholdAlarm(self, data, destination):
             if(self.calculateAverage(data) < self.threshold and self.belowThreshold):
                        message = "Average below acceptable amount for " + self.subjectName + "."
                        self.sendEmail(destination, message, "Alert: Average performance below threshold.")

    def aboveThresholdAlarm(self, data, destination):
        if(self.calculateAverage(data) > self.threshold and self.aboveThreshold):
                message = "Average above acceptable amount for " + self.subjectName + "."
                self.sendEmail(destination, message, "Alert: Average performance above threshold")

    def isMissingDataAlarm(self, animals):
        if(self.missingData and len(animals) != 0):
            for animal in animals:
                for destination in alarm_settings.contact_dict[animal]:
                    self.sendEmail(destination, "Missing data for " + animal + ".", "Alert: Missing data")

    def alert(self):
        animals = alarm_settings.contact_dict.keys()
        self.loadData(animals)

        for path, data in self.behavData:
            self.parseFilePath(path)
            if self.subjectName in animals:
                animals.remove(self.subjectName)

                for destination in alarm_settings.contact_dict[self.subjectName]:
                    self.belowThresholdAlarm(data, destination)
                    self.aboveThresholdAlarm(data, destination)

        self.isMissingDataAlarm(animals)
        
    def calculateAverage(self, data):
        nValidTrials        = data['nValid'][-1]
        nRewardTrials       = data['nRewarded'][-1]
        return float(nRewardTrials)/nValidTrials
