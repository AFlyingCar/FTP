#################
#Tyler Robbins	#
#1/19/14	#
#FTPConnect	#
#################

import urllib2
import os
from ftplib import FTP
from getpass import getpass

ulogin = True

ftp = FTP('ftp.tylerclay.com') #connects to website

user = raw_input(">>> UserName: ") #gets username
passw = getpass(">>> Password: ") #gets password

while ulogin:
	try:
		ftp.login(user, passw) #tries to input username and password
		ulogin = False
	except(Exception): #catches login error
		print ">>> Incorrect login."
		exit()

ftp.cwd('www.tylerclay.com')
#print "Permissions", "Date Updated", "Files"
ftp.retrlines('LIST') #list all directories

while True:
	loc = raw_input('>>> ') #user lists commands
		
	try:
		if loc.upper() == 'EXIT': #exits program
			exit()

		elif loc.split(" ")[0] == 'cd':
			loc = loc.split(" ")

			try:
				ftp.cwd(loc[1]) #changes directory to loc
			except(Exception):
				print "Could not find ", loc[1], ". Destination does not exist."
		
		elif loc == 'ls': #lists directories and files
			ftp.retrlines('LIST')
		
		elif loc.split(" ")[0] == 'mkdir':
			loc = loc.split(" ")

			try:
				os.mkdir(loc[1])

			except(Exception):
				print "Destination already exists"

	except(Exception):
		print loc , ": Command not found."

nuclear = u'\u2622'
