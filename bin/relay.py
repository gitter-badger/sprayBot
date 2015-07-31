#!/usr/bin/env python2.7

import RPi.GPIO as GPIO
import sys
import os
import subprocess
import re
import signal
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from datetime import datetime

#############################
# global declarations
#############################
DEBUG=0
APPDIR = "/appli"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RELAY1 = 17 # gpio pin
RELAY2 = 18 # gpio pin

# Set relay pins as output
GPIO.setup(RELAY1, GPIO.OUT)
GPIO.setup(RELAY2, GPIO.OUT)

# email declarations
sender = 'spraybot@issany.net'
dest = ['root@localhost']

#############################
# class
#############################
class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	ERROR = '\033[91m'
	ENDC = '\033[0m'
	DEBUG = '\033[94m'

#############################
# functions
#############################
''' get pin status '''
def getState(pin):
	return GPIO.input(pin)

''' log message '''
def logMsg(level,msg):
	date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

	if level == "INFO":
		color = bcolors.OK
	if level == "WARN":
		color = bcolors.WARNING
	if level == "ERROR":
		color = bcolors.ERROR
	if level == "DEBUG":
		color = bcolors.DEBUG

	if DEBUG == 1:
		if level == "DEBUG":
			print date + " ["+ color + "DEBUG" + bcolors.ENDC + "] " + msg
		else:
			print date + " [" + color + level + bcolors.ENDC + "] " + msg
	else:
		if level != "DEBUG":
			print date + " [" + color + level + bcolors.ENDC + "] " + msg

''' send email '''
def sendEmail():
	m = MIMEMultipart()
	m['Subject'] = '[SPRAYBOT] You have a notification'
	m['From'] = sender
	m['To'] = dest

	s = smtplib.SMTP('localhost')
	s.sendmail(sender, dest, m.as_string())
	s.quit()

#############################
# get args
#############################
if len(sys.argv) < 3:
	logMsg("WARN","Usage: " + os.path.basename(sys.argv[0]) + " <1|2> <on|off>")
	sys.exit()

relayNumber = int(sys.argv[1])
relayStatus = sys.argv[2].lower()

if relayNumber not in [1,2]:
	logMsg("WARN","Usage: " + os.path.basename(sys.argv[0]) + " <1|2> <on|off>")
	sys.exit()

if relayNumber == 1:
	relayNumber = RELAY1
if relayNumber == 2:
	relayNumber = RELAY2

if relayStatus not in ["on","off"]:
	logMsg("WARN","Usage: " + os.path.basename(sys.argv[0]) + " <1|2> <on|off>")
	sys.exit()

#############################
# main program
#############################
if __name__=='__main__':
	try:
		logMsg("INFO","Starting program")
		logMsg("INFO","Executing command: relay " + str(relayNumber) + " : " + relayStatus)
		logMsg("DEBUG", "relay " + str(relayNumber) + " - status " + relayStatus)
		if relayStatus == "on":
			GPIO.output(relayNumber, GPIO.LOW)
		if relayStatus == "off":
			GPIO.output(relayNumber, GPIO.HIGH)

		if getState(relayNumber) == 0:
			logMsg("DEBUG","The new state of " + str(relayNumber) + " is ON")
		else:
			logMsg("DEBUG","The new state of " + str(relayNumber) + " is OFF")


		f = open(APPDIR + '/tmp/relayState.txt', 'w')
		f.write(str(RELAY1) + ':' + str(getState(RELAY1)) + "\n")
		f.write(str(RELAY2) + ':' + str(getState(RELAY2)) + "\n")
		f.close()
		'''sendEmail()'''

		logMsg("INFO","exiting ... bye bye")

	except RuntimeError,e:
		logMsg("CRITICAL","Failed to execute command: " + e.message)
		logMsg("INFO","exiting ... bye bye")
		sys.exit()
