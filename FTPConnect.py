#################
#Tyler Robbins	#
#1/19/14	#
#FTPConnect	#
#################

import os, sys
from ftplib import FTP
from getpass import getpass
import urllib, urllib2
ulogin = True

ftp = FTP('ftp.tylerclay.com') #connects to website
user = raw_input(">>> UserName: ") #gets username

while ulogin:
	passw = getpass(">>> Password: ") #gets password

	try:
		ftp.login(user, passw) #tries to input username and password
		ulogin = False
		
	except Exception as e: #catches login error
		if str(e) == '530 Login incorrect.':
			print ">>> Incorrect login."
		else:
			print ">>> " + str(e)
		i=0
		i+=1
		if i >= 5:
			print "quitting"
			ftp.quit()
			sys.exit()

ftp.cwd('www.tylerclay.com')

print "Permissions", "                                         Last Updated", "Files"
ftp.retrlines('LIST') #list all directories

while True:
	choice = raw_input('>>> ') #user lists commands
		
	try:
		if choice.lower() == 'exit': #exits program
			ftp.quit()
			exit()
		
		elif choice.lower() == 'help': #prints help for the user
			print """cd [destination]
upload [source] [file name]
download [name]
exit
help
ls {directory}
mkdir [name]
rmdir [name]
"""

		elif choice.split(" ")[0] == 'cd':
			cd = choice.split(" ", 1)
			cd.remove("cd")

			try:
				if "/" in cd:
					cd = cd.split("/")
			
				for item in cd:
					ftp.cwd(item) #changes to directory of choice

			except(Exception):
				print "Could not find '" + choice.split(" ")[1] + "'. Destination does not exist."
		
		elif choice.split(" ")[0] == 'ls': #lists directories and files
			try:
				loc = ftp.pwd()
				
				if " " in choice:
					choice = choice.split(" ", 1)
					choice = choice[1].split("/")
						
					for item in choice:
						ftp.cwd(item) #allows the user to list in a separate directory
				
				print "Permissions", "                                         Last Updated", "Files"
				ftp.retrlines('LIST')
				ftp.cwd(loc)

			except(Exception):
				print "Could not find '" + choice.split(" ")[1] + "'. Destination does not exist."
		
		elif choice.split(" ")[0] == 'mkdir': #makes directory
			choice = choice.split(" ")

			try:
				ftp.mkd(choice[1])

			except(Exception):
				print "Destination already exists."

		elif choice.split(" ")[0] == 'rmdir': #removes directory
			ask = raw_input("Warning! This action cannot be undone. Do you wish to continue?(y/n) ")

			if ask == 'y':
				try:
					ftp.rmd(choice.split(" ")[1])
				except(Exception):
					print "Could not remove '" + choice.split(" ")[1] + "'. Destination does not exist."

		elif choice.split(" ")[0] == 'upload': #copies file
			choice = choice.split(" ")
			loc = choice[1]
			name = choice[2]
		
			try:

				upload = open(loc + name, 'rb') #opens file
				ftp.storbinary('STOR ' + name, upload) #sends file
		
				upload.close() #closes file

			except(Exception):
				print "Could not find '" + name + "' in '" + loc + "'."
		
		elif choice.split(" ")[0] == 'download':
			choice = choice.split(" ", 1)
			print choice
			print ftp.pwd()

			try:
				loc = raw_input("Type the destination path for where you want to save " + choice[1] + ". C:\\") #get save location from the user
				
				x = open("C:\\" + loc + "\\" + choice[1], 'wb') #open file for writing
				ftp.retrbinary('RETR ' + choice[1], x.write)
				x.close()

			except(Exception):
				print "Error. File " + choice[1] + " not found."
		else:
			print "'" + choice + "': Command not found."
		
		if choice == '`':
			sys.exit()

	except(Exception): #catches errors that make it past other error handlers
		pass

nuclear = u'\u2622'