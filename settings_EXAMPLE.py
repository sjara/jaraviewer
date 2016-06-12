#!/usr/bin/env python

'''
Settings for the Jaraviewer
'''

IMAGE_PATH = '/tmp/'             # Path to save the generated plots

SUBJECTS_FILE = './static/subjects.txt' # File to store subject names

PROFILES_FILE = "./static/profiles.txt" # File to store profiles

JARAVIEWER_PORT_NAME = "/jaraviewer"    # URL for entering the jaraviewer on a server

JARAVIEWER_PORT_NUMBER = 8080           # PORT NUMBER FOR JARAVIEWER

JARAVIEWER_LOCAL_ADDRESS = '0.0.0.0'    # The local IP address for flask, use the default '0.0.0.0' if it is installed on a server.
