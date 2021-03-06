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
    import urllib.error
except ImportError:
    from urllib2 import urlopen
    import urllib2.error
from xml.dom import minidom
import sys
import time
import argparse

description = 'NowPlayingToTxt.py is a python script which periodically \
checks for changes to a user\'s now playing information on last.fm and \
updates a text file containing information for the currently playing track. \
Copyright (C) 2014  Alex Phillips'

#Change this
api_key = api_key='17fbcb642c7354767cef8f24a3b2725d'

local_copy = 'nowplaying.xml'
filename = 'nowplaying.txt'

#Putting defaults at top of file for reference
defaults = dict()
defaults['prepend'] = 'Now playing: '
defaults['append'] = '                '
defaults['delay'] = 5

args = dict()

def main():
    get_parameters()
    
    print('Starting with arguments:')
    print('Username: ' + args['username'])
    print('Prepended text: ' + args['prepend'])
    print('Appended text: ' + args['append'])
    print('Delay between updates: ' + str(args['delay']))
    
    #Keeping track of the last track that was playing using track url
    last_track = ''
    
    feed_url = ('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='
    + args['username'] + '&api_key=' + api_key + '&limit=1')
    
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
                
                track_data= args['prepend'] + artist + ' - ' + track + args['append']
                
                print(track_data)
                
                #Update file
                output = open(filename, 'w')
                output.write(track_data)
                output.close()
                
        #Else, nothing playing
        else:
            #If only just stopped playing
            if(last_track != ''):
                
                last_track = ''
                track_data = ''
                
                output = open(filename, 'w')
                output.write(track_data)
                output.close()
                
        #Need to wait at least 1 second for another API call
        time.sleep(args['delay'])

#Get command line arguments
def get_parameters():
    parser = argparse.ArgumentParser(prog='NowPlayingToTxt',description=description)
    parser.add_argument('username')
    parser.add_argument('-p', '--prepend', dest = 'prepend', default = defaults['prepend'])
    parser.add_argument('-a', '--append', dest = 'append', default = defaults['append'])
    parser.add_argument('-d', '--delay', dest = 'delay', default = defaults['delay'], type=int)
    
    input = parser.parse_args()
        
    args['username'] = input.username
    args['prepend'] = input.prepend
    args['append'] = input.append
    if input.delay < 1:
        print('#'*20)
        print('Delay must be AT LEAST 1 second, setting to 1 second')
        print('#'*20)
        args['delay'] = 1
    else:
        args['delay'] = input.delay
        

        
#Download xml as binary
def download(url,filename):
    try:
        instream=urlopen(url)
        outfile=open(filename,'wb')
        for chunk in instream:
            outfile.write(chunk)
        instream.close()
        outfile.close()
    except Exception as e:
        print(e)
        sys.exit()

if __name__=="__main__":
    main()
