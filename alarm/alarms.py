from alarm import Alarm

"""
This file will be run as a cron job at midnight of every night. Make sure to setup
the alarm_settings file and do a test run before adding the run_alarm.sh script as
a cron job. Below are example full examples -- to run the examples, simply uncomment
everything below this text.

# Example alarm creation:

belowThreshold = Alarm(threshold = 0.5, belowThreshold = True)
aboveThreshold = Alarm(threshold = 0.7, aboveThreshold = True)
missingData    = Alarm(missingData = True)
aboveAndBelow  = Alarm(threshold = 0.6, belowThreshold = True, aboveThreshold = True)

# Load data in for alarms:

belowThreshold.loadData()
aboveThreshold.loadData()
missingData.loadData()
aboveAndBelow.loadData()

# Run the alert method (checks all data for any issues, and sends out email if issues are found):

belowThreshold.alert()
aboveThreshold.alert()
missingData.alert()
aboveAndBelow.alert()
"""

# Define alarms below. 


