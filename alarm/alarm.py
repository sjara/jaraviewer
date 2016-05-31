#!/usr/bin/env python
import os
import logging
import alarm_settings
from jaratoolbox import settings
from jaratoolbox import loadbehavior
from jaratoolbox import behavioranalysis
from jaratoolbox import extrafuncs

from datetime import date
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

class Alarm(object):
    """
    A class that allows you to define a new alarm that will send
    an email when given conditions are true.
    """

    def __init__(self, threshold = 0, subjects = [], subscribers = [], log = False, belowThreshold = False, aboveThreshold = False, missingData = False):

        """
        Sets up instance variables that will be needed later on, and sets
        all objects passed in to the relevent instance variables.

        Args:
            threshold       - The threshold to check against for the belowThreshold/aboveThreshold alarms
            subjects        - A list of strings containing the names of animals to check the data for
            subscribers     - A list of strings containing the emails of those to alert when alarms are set off
            log             - A boolean flag on whether to keep a log of debug/error/info messages
            belowThreshold  - A boolean flag to check if animals are below the passed in threshold 
            aboveThreshold  - A boolean flag to check if animals are above the passed in threshold 
            missingData     - A boolean flag to check if data for the passed in animals is missing
        Returns:
            A new Alarm object
        """

        self.behavData      = [] 

        # Flags for certain alarms
        self.threshold      = threshold
        self.belowThreshold = belowThreshold
        self.aboveThreshold = aboveThreshold
        self.missingData    = missingData
        self.subjects       = subjects
        self.subscribers    = subscribers
        self.log            = log

        # Information from parsed filepath
        self.subjectName        = None
        self.experimentData     = None
        self.paradigm           = None
        self.experimenterName   = None
        self.experimentDate     = None

        if(self.log):
            logging.basicConfig(filename = alarm_settings.LOG_FILENAME, level = logging.INFO)

    def loadData(self):
        """
        Walks through all files in settings.BEHAVIOR_PATH and lazily loads in the
        relevent files to the "behavData" list where each index is a tuple formatted as, 
        (<full path of file>, <loaded behavior data>).

        Args:
            None
        Returns:
            None
        """

        for info in os.walk(settings.BEHAVIOR_PATH):
            path = info[0]

            # Get the files, if there are any
            for element in info[2]:
                split           = element.split(".")

                # If there's only one '.' in the filename, then we know it's not a .old.h5 file, or a file without an extension.
                if(len(split) == 2):
                    name, extension = element.split(".")

                    if(self.log):
                        logging.debug("Name: " + name + " Extension: " + extension)

                    for animal in self.subjects:

                        # Get the date from the name and format it in ISO format to compare to the current date.
                        experimentDate  = name.split("_")[-1]
                        isoDate         = experimentDate[:4] + "-" + experimentDate[4:6] + "-" + experimentDate[6:8]
                        today           = date.today() 

                        if(self.log):
                            logging.debug("Comparing date: " + str(isoDate) + " to " + str(today) + " (today)")

                        # We only want data from today from an animal that we care about
                        if(today == extrafuncs.parse_isodate(isoDate) and extension == "h5" and animal in name):
                            try:
                                full_path = os.path.join(path, element)
                                self.behavData.append((full_path, loadbehavior.BehaviorData(full_path, readmode='full')))
                                if(self.log):
                                    logging.info("Successfully loaded data from: " + full_path)
                            except:
                                self.sendToAllSubscribers("Error when attempting to load " + full_path + ".", "Alert: Alarm error")
                                if(self.log):
                                    logging.error("Could not load " + full_path + ".")

    def parseFilePath(self, filepath):
        """
        Parses a given filepath and sets the internal variables to the correct parts.

        Args:
            filepath - The filepath to parse
        Returns:
            None
        """

        li                      = filepath.split("/") 
        last                    = li[-1].split("_")

        self.subjectName        = li[-2]
        self.experimenterName   = li[-3]
        self.experimentDate     = last[-1]
        self.paradigm           = last[-2]
        self.subjectName        = last[-3]

    def sendToAllSubscribers(self, message, subject):
        """
        Sends the given message and subject to all subscribers in the subscribers list passed in
        when the object was created. 
        
        Args:
            message - The message to send
            subject - The subject of the message
        Returns:
            None
        """

        for destination in self.subscribers:
            if(self.log):
                logging.info("Sending " + message + " to " + destination)

            self.sendEmail(destination, message, subject)

    def sendEmail(self, destination, message, subject):
        """
        Sends an email using the user/pass in auth.txt and using the UOregon SMTP server. 

        Args:
            destination - The receivers email address
            message     - The body of the email
            subject     - The subject of the email
        Returns:
            None
        """

        smtpServer          = "smtp.uoregon.edu"
        textSubtype         = "plain"

        f                   = open(alarm_settings.path_to_auth)
        text                = f.read()
        sender, password    = text.split()

        # Setup message variables 
        msg             = MIMEText(message)
        msg['Subject']  = subject
        msg['From']     = sender

        # Because we don't have an email set up yet, just print out what we would have sent.
        print("To: " + destination)
        print("From: " + sender)
        print("Subject: " + subject)
        print("Body: " + message + "\n")

        """
        # Setup the connection, and attempt to send the message.
        conn            = SMTP(smtpServer)
        conn.set_debuglevel(False)
        conn.login(sender, password)
        conn.sendmail(sender, destination, msg.as_string())
        conn.close()

        if(self.log):
            logging.info("Successfully sent alert to " + destination) 
        """

    def belowThresholdAlarm(self, data):
        """
        Sends out an email to all subscribers if the belowThreshold flag is true
        and the average performance of the animal (as calculated by calculateAverage)
        is below the set threshold.

        Args:
            data - The data to calculate the average on
        Returns:
            None
        """

        if(self.belowThreshold and self.calculateAverage(data) < self.threshold):
                    message = "Average below acceptable amount for " + self.subjectName + "."
                    if(self.log):
                        logging.info(message)

                    self.sendToAllSubscribers(message, "Alert: Average performance below threshold.")

    def aboveThresholdAlarm(self, data):
        """
        Sends out an email to all subscribers if the aboveThreshold flag is true
        and the average performance of the animal (as calculated by calculateAverage)
        is above the set threshold.

        Args:
            data - The data to calculate the average on
        Returns:
            None
        """

        if(self.calculateAverage(data) > self.threshold and self.aboveThreshold):
                message = "Average above acceptable amount for " + self.subjectName + "."
                if(self.log):
                    logging.info(message)

                self.sendToAllSubscribers(message, "Alert: Average performance above threshold.")

    def isMissingDataAlarm(self):
        """
        Sends out an email to all subscribers if the missingData flag is true
        and there is no data for a particular animal.

        Args:
            None
        Returns:
            None
        """

        if(self.missingData and len(self.subjects) != 0):
            for animal in self.subjects:
                message = "Missing data for " + animal + "."
                if(self.log):
                    logging.info(message)
                self.sendToAllSubscribers(message, "Alert: Missing data")

    def alert(self):
        """
        Loads in the necessary data and iterates through it calling all alarms on
        that data.

        Args:
            None
        Returns:
            None
        """

        self.loadData()

        for path, data in self.behavData:
            self.parseFilePath(path)

            # Only call the alarms on animals that we care about.
            if(self.subjectName in self.subjects):
                if(self.log):
                    logging.debug("Using data from " + self.subjectName)

                self.subjects.remove(self.subjectName)

                self.belowThresholdAlarm(data)
                self.aboveThresholdAlarm(data)

        self.isMissingDataAlarm()
        
    def calculateAverage(self, data):
        """
        Calculates the average performance of a given dataset. 

        Args:
            data - The data to calculate the average on
        Returns:
            The average performance as a float.
        """

        nValidTrials        = data['nValid'][-1]
        nRewardTrials       = data['nRewarded'][-1]
        return float(nRewardTrials)/nValidTrials
