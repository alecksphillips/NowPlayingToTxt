#!/usr/bin/env python
#
# NowPlayingToTxt.py is a python script which periodically checks for changes to
# a user's now playing information on last.fm and updates a text file containing
# information for the currently playing track.
# Copyright (C) 2014  Alex Phillips
#

#########################
# GPL Information
#########################
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for more information
#
#########################

#Check for changes
#Update to text file

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from xml.dom import minidom
import os.path
import sys
import time

username = 'alecksphillips'
api_key = api_key='8cf8b8f0778a606621666c2152df79db'

local_copy = 'nowplaying.xml'
filename = 'nowplaying.txt'
prepend = 'Now playing :'
url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=' + username + '&api_key=' + api_key

#Main loop
def main():
	trackurl = ''

	while True:
		download(url,local_copy)
		
		data=open(local_copy,'rb')
		xmldoc=minidom.parse(data)
		data.close()
		
		item = xmldoc.getElementsByTagName('track')[0]
		
		#If track playing
		if (item.attributes.item(0)):
			#If track changed
			if (item.getElementsByTagName('url') != trackurl):
				#Track has changed, update file
				trackurl = item.getElementsByTagName('url')[0].firstChild
				artist = item.getElementsByTagName('artist')[0].firstChild.data
				track = item.getElementsByTagName('name')[0].firstChild.data
			
				output = open(filename, 'w')
				output.write(prepend + artist + ' - ' + track)
				output.close()
		else:
			output = open(filename, 'w')
			output.write('')
			output.close()
		time.sleep(1)
	
	
def download(url,filename):
    instream=urlopen(url)
    outfile=open(filename,'wb')
    for chunk in instream:
        outfile.write(chunk)
    instream.close()
    outfile.close()


	
if __name__=="__main__":
    main()
