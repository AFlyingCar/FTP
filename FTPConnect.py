#################
#Tyler Robbins	#
#1/19/14	#
#FTPConnect	#
#################

import sys, os
from ftplib import FTP
from getpass import getpass


while True:
	ulogin = True
	url = raw_input(">>> FTP server (example.com) or (ip.ip.ip:anIP): ") #gets website/server from user

	try:
		ftp = FTP("ftp." + url) #Allows the user to choose what server to connect to
		break

	except Exception as e:
		if str(e) == '[Errno 11001] getaddrinfo failed':
			print "Could not find '" + str(url) + "'."
		
		else:
			print str(e)

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
			print ">>> Incorrect " + i + " times. Closing connection."

			ftp.quit()
			sys.exit()

#ftp.cwd('www.tylerclay.com')

print "Permissions", "                                         Last Updated", "Files/Folders"
ftp.retrlines('LIST') #list all directories

while True:
	choice = raw_input('>>> ') #user lists commands
	try:
		if choice.lower() == 'exit': #exits program
			ftp.quit()
			exit()

		elif choice.lower() == 'help': #prints help for the user
			print """cd [destination]
upload [file location]
download [name]
exit
help
ls {directory}
mkdir [name]
rmdir [name]
cdir
"""

		elif choice.split(" ")[0] == 'cd':
			cd = choice.split(" ", 1)
			cd.remove("cd")

			try:
				if "/" in cd:
					cd = cd.split("/")
			
				for item in cd:
					ftp.cwd(item) #changes to directory of choice

			except Exception as e:
				if str(e) == 'FileNotFoundError':
					print ">>> Could not find '" + choice.split(" ")[1] + "'. Destination does not exist."
				else:
					print str(e)
		
		elif choice.split(" ")[0] == 'ls': #lists directories and files
			try:
				loc = ftp.pwd()
				
				if " " in choice:
					choice = choice.split(" ", 1)
					choice = choice.split(" ", 1).split("/")
						
					for item in choice:
						ftp.cwd(item) #allows the user to list in a separate directory
				
				print "Permissions", "                                         Last Updated", "Files"
				ftp.retrlines('LIST')
				ftp.cwd(loc)

			except(Exception):
				print ">>> Could not find '" + choice.split(" ")[1] + "'. Destination does not exist."
		
		elif choice.split(" ")[0] == 'mkdir': #makes directory
			choice = choice.split(" ")

			try:
				ftp.mkd(choice[1]) #create specified directory

			except(Exception):
				print ">>> Destination already exists."

		elif choice.split(" ")[0] == 'rmdir': #removes directory
			ask = raw_input(">>> Warning! This action cannot be undone. Do you wish to continue?(y/n) ") #ask user for confirmation to continue

			if ask == 'y':
				try:
					ftp.rmd(choice.split(" ")[1]) #remove specified directory

				except(Exception):
					print ">>> Could not remove '" + choice.split(" ")[1] + "'. Destination does not exist."

		elif choice.split(" ")[0] == 'upload': #copies file
			loc = choice.split(" ")[1]
			name = loc.split("\\")[len(loc.split("\\")) - 1] #uploads file with same name as the original

			try:
				upload = open(loc, 'rb') #opens file
				ftp.storbinary('STOR ' + name, upload) #sends file
				ftp.sendcmd("TYPE i")

				if ftp.size(name) != upload.tell():
					wait =  upload.tell() - ftp.size(name)
					time.sleep(wait)

				upload.close() #closes file

			except(Exception):
				print ">>> Could not find '" + name + ".' in '" + loc + "'."
		
		elif choice.split(" ")[0] == 'download':
			choice = choice.split(" ", 1)
			try:
				print "Current working directory: " + str(os.getcwd())
				loc = raw_input("Type the destination path for where you want to save " + choice[1] + ". C:\\") #get save location from the user
				x = open("C:\\" + loc + "\\" + choice[1], 'wb') #open file for writing
				ftp.retrbinary('RETR ' + choice[1], x.write)
				ftp.sendcmd("TYPE i")

				if x.tell() != ftp.size(choice[1]):
					wait = ftp.size(choice[1]) - x.tell()
					time.sleep(wait)
				
				x.close()

			except(Exception):
				print ">>> Error. File " + choice[1] + " not found."

		elif choice == 'currdir':
			print ">>> Current os directory: ",
			print str(os.getcwd())

		elif choice == 'chdir':
			print ">>> Current working directory:",
			print str(os.getcwd())

			loc = raw_input(">>> C:\\ ")
			os.chdir("C:\\\\" + loc)

		else:
			print ">>> '" + choice + "': Command not found."
		
		if choice == '`':
			sys.exit()

	except Exception as e: #catches errors that make it past other error handlers
		if str(e) == "[Errno 10053] An established connection was aborted by your host machine":
			ftp.quit()
			sys.exit()

		elif str(e) == "421 No transfer timeout (600 seconds): closing control connection":
			print "No file transfer for 600 seconds. Closing connection."
			ftp.quit()
			sys.exit()

		else:
			print ">>> " + str(e)

nuclear = u'\u2622'
print nuclear