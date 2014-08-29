NowPlayingToTxt
===============

[![Build Status](https://travis-ci.org/alecksphillips/NowPlayingToTxt.png?branch=master)](https://travis-ci.org/alecksphillips/NowPlayingToTxt)

NowPlayingToTxt.py is a python script which periodically checks for
changes to a user's now playing information on last.fm and updates a
text file containing information for the currently playing track.
Copyright (C) 2014  Alex Phillips

Usage
-----

`python NowPlayingToTxt.py USERNAME [-p 'prepended text'] [-a 'appended text'] [-d delay]`

TODO
----
Add testing (coveralls)
Add more detailed information on errors (e.g. 'Username may be spelt incorrectly')
Add detailed information under help command (-h, --help)

GPL
---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/> for more information

