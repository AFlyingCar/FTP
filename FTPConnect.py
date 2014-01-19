#################
#Tyler Robbins	#
#1/19/14	#
#FTPConnect	#
#################

import urllib2
from ftplib import FTP
from getpass import getpass

ftp = FTP('ftp.tylerclay.com')

user = raw_input(">>> UserName: ")
passw = getpass(">>> Password: ")

ulogin = True

while ulogin:
	try:
		ftp.login(user, passw)
		ulogin = False
	except(Exception):
		print ">>> Incorrect login."
		exit()

ftp.cwd('www.tylerclay.com')
ftp.retrlines('LIST')

while True:
	loc = raw_input('>>> ')
	
	if loc.upper() == 'EXIT':
		exit()

	ftp.cwd(loc)
	ftp.retrlines('LIST')

