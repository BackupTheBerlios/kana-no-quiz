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
from distutils.core import setup
import os.path, glob, sys

if 'bdist_wininst' in sys.argv:
	scriptfiles = glob.glob(os.path.join('data','script','*.py*'))
else: scriptfiles = []

#Common data files.
datafiles = [
		#Textual files.
		(os.path.join('share','kana-no-quiz'),glob.glob("*.txt")),
		#Images (per extention adding).
		(os.path.join('share','kana-no-quiz','img'),glob.glob(os.path.join("data","img","*.png"))+
			glob.glob(os.path.join("data","img","*.gif"))+
			glob.glob(os.path.join("data","img","*.xbm"))),
		(os.path.join('share','kana-no-quiz','img','kana'),glob.glob(os.path.join("data","img","kana","*.gif"))),
		#Localisation.
		(os.path.join('share','kana-no-quiz','locale','fr','LC_MESSAGES'),[os.path.join("data","locale","fr","LC_MESSAGES","kana-no-quiz.mo")]), #French
		(os.path.join('share','kana-no-quiz','locale','pt_BR','LC_MESSAGES'),[os.path.join("data","locale","pt_BR","LC_MESSAGES","kana-no-quiz.mo")]), #Portuguese of Brazil
		(os.path.join('share','kana-no-quiz','locale','sr','LC_MESSAGES'),[os.path.join("data","locale","sr","LC_MESSAGES","kana-no-quiz.mo")]), #Serbian
		(os.path.join('share','kana-no-quiz','locale','sv','LC_MESSAGES'),[os.path.join("data","locale","sv","LC_MESSAGES","kana-no-quiz.mo")])] #Swedish
if 'bdist_wininst' in sys.argv: #Da Windows icon!
	datafiles.append((os.path.join("share","kana-no-quiz","img"),[os.path.join("data","img","icon.ico")]))

setup(
	name			=	'Kana no quiz',
	version			=	'1.5cvs',
	description		=	'A kana memorization tool.',
	author			=	'Choplair-network',
	author_email	=	'contact@choplair.org',
	url				=	'http://www.choplair.org/',
	download_url	=	'http://developer.berlios.de/project/filelist.php?group_id=1783',
	license			=	'GNU General Public License',
	packages		=	['kana-no-quiz'],
	package_dir		=	{'kana-no-quiz': 'data/py'},
	scripts			=	scriptfiles,
	data_files		=	datafiles
	)

if "install" in sys.argv:
	# Post install stuff (Unix).
	if os.name=="posix":
		exec_script = "/usr/local/bin/kana-no-quiz"
		print "Putting Kana no quiz executable script into `%s'." % os.path.dirname(exec_script)
		do("cp ./data/py/__init__.py %s; chmod +x %s" % (exec_script,exec_script))
