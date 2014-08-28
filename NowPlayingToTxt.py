#!/usr/bin/env python
#
# NowPlayingToTxt.py is a python script which periodically checks for
# changes to a user's now playing information on last.fm and updates a
# text file containing information for the currently playing track.
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

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from xml.dom import minidom
import sys
import time

#Change this unless you want my terrible taste on your feed
username = 'alecksphillips'
api_key = api_key='17fbcb642c7354767cef8f24a3b2725d'

local_copy = 'nowplaying.xml'
filename = 'nowplaying.txt'
prepend = 'Now playing: '
append = '                '
feed_url = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
    + username + '&api_key=' + api_key)

def main():
    #Keeping track of the last track that was playing using track url
    last_track = ''

    while True:
        download(feed_url,local_copy)
        
        data=open(local_copy,'rb')
        xmldoc=minidom.parse(data)
        data.close()
        
        item = xmldoc.getElementsByTagName('track')[0]
        
        #If track playing
        if (item.attributes.item(0)):
        
            current_track = item.getElementsByTagName('url')[0].firstChild.data
            
            #If track changed
            if (current_track != last_track):
            
                last_track = current_track
                artist = item.getElementsByTagName('artist')[0].firstChild.data
                track = item.getElementsByTagName('name')[0].firstChild.data
                
                track_data= prepend + artist + ' - ' + track + append
                
                #Update file
                output = open(filename, 'w')
                output.write(track_data)
                output.close()
                
        #Else, nothing playing
        else:
            #If only just stopped playing
            if(last_url != ''):
                
                last_url = ''
                track_data = ''
                
                output = open(filename, 'w')
                output.write(track_data)
                output.close()
                
        #Need to wait 1 second for another API call
        time.sleep(1)

#Download xml as binary        
def download(url,filename):
    instream=urlopen(url)
    outfile=open(filename,'wb')
    for chunk in instream:
        outfile.write(chunk)
    instream.close()
    outfile.close()

if __name__=="__main__":
    main()
