#!/usr/bin/env python
"""Kana no quiz!

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
# Psyco module (Just in time compiler)
try:
	import psyco
except ImportError:
	pass
else:
		print "Loading psyco...",
		psyco.full()
		print "psyco loaded."

# Imports.
import sys
from os import path, chdir, environ
import options
import gtk_gui as gui

# Global variables.
VERSION = "2.0 CVS"

# Setting Kana no quiz's data root directory's path.
datarootpath = path.join(sys.prefix, 'share', 'kana-no-quiz')

options = options.Options()
options.read_from_file()

# Setting the `$LANG' as it is set in the configuration file.
environ['LANG'] = options['lang']

# Let's go!
gui = gui.Gui(options, VERSION, datarootpath)
gui.main()

