from alarm import Alarm 

"""
This file will be run as a cron job at midnight of every night. Make sure to setup
the alarm_settings file and do a test run before adding the run_alarm.sh script as
a cron job. Below are example full examples -- to run the examples, simply uncomment
everything below this text.

# Example alarm creation:

belowThreshold = Alarm(threshold = 1, belowThreshold = True, subjects = ["adap022"], subscribers = ["foo@uoregon.edu", "bar@uoregon.edu"])
aboveThreshold = Alarm(threshold = 0.0, aboveThreshold = True, subjects = ["adap021"], subscribers = ["aboveThreshold@uoregon.edu"])
missingData    = Alarm(missingData = True, log = True, subjects = ["thisAnimalDoesn'tExist"], subscribers = ["missingDataAlert@uoregon.edu"])
aboveAndBelow  = Alarm(threshold = 0.6, belowThreshold = True, aboveThreshold = True, subjects = ["adap022", "adap021"], subscribers = ["aboveAndBelow@uoregon.edu", "johnnyAppleseed@uoregon.edu"])

# Run the alert method (checks all data for any issues, and sends out email if issues are found):

belowThreshold.alert()
aboveThreshold.alert()
missingData.alert()
aboveAndBelow.alert()
"""

# Define alarms below. 
    
