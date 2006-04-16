#!/usr/bin/env python
"""
Kana no quiz!
Copyleft 2003, 2004, 2005, 2006 Choplair-network.
$Id$

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
import sys
from os import path, chdir, environ

VERSION = "1.5cvs"

#Setting Kana no quiz's data root directory's path.
datarootpath = path.join(sys.prefix,'share','kana-no-quiz')

import options
options = options.Options()
options.read()

#Set the $LANG as it is set in the configuration file.
environ['LANG'] = options.val('lang')

#
# Choice of the interface.
#
try: arg = sys.argv[1]
except: arg = str()

if arg=="-tk": import tkinter_gui as gui
elif arg=="-gtk": import gtk_gui as gui
else:
	try: 	import gtk_gui as gui
	except: import tkinter_gui as gui

#Let's go!
gui = gui.Gui(options,VERSION, datarootpath)
gui.main()