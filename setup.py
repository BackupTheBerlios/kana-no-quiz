#!/usr/bin/env python
"""Kana no quiz!

   Copyleft 2003, 2004, 2005, 2006, 2007 Choplair-network.
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
import os
import glob
import sys
from distutils.core import setup
try: import py2exe
except: pass

if 'bdist_wininst' in sys.argv:
   scriptfiles = glob.glob(os.path.join('data', 'script', '*'))    
elif "install" in sys.argv:
   scriptfiles = [os.path.join("data", "script", "kana-no-quiz")]
else: scriptfiles = []

# Common data files.
datafiles = [
      # Textual files.
      (os.path.join('share', 'kana-no-quiz'), glob.glob("*.txt")),
      # Images (per extention addition).
      (os.path.join('share', 'kana-no-quiz', 'img'),
         glob.glob(os.path.join("data", "img", "*.png"))+
         glob.glob(os.path.join("data", "img", "*.xbm"))),
      (os.path.join('share', 'kana-no-quiz', 'img', 'kana', 'choplair'),
         glob.glob(os.path.join("data", "img", "kana", "choplair",
         "*.png"))),
      (os.path.join('share', 'kana-no-quiz', 'img', 'kana', 'kanatest'),
         glob.glob(os.path.join("data", "img", "kana", "kanatest",
         "*.png"))),
      # Sounds.
      (os.path.join('share', 'kana-no-quiz', 'sound', 'kana_female'),
         glob.glob(os.path.join("data", "sound", "kana_female", "*.wav"))),
      # Localization.
      (os.path.join('share', 'kana-no-quiz', 'locale', 'de', 'LC_MESSAGES'),
         [os.path.join("data", "locale", "de", "LC_MESSAGES",
         "kana-no-quiz.mo")]),  # German
      (os.path.join('share', 'kana-no-quiz','locale', 'fr', 'LC_MESSAGES'),
         [os.path.join("data", "locale", "fr", "LC_MESSAGES",
         "kana-no-quiz.mo")]),  # French
      (os.path.join('share', 'kana-no-quiz','locale', 'pt_BR', 'LC_MESSAGES'),
         [os.path.join("data", "locale", "pt_BR", "LC_MESSAGES",
         "kana-no-quiz.mo")]),  # Portuguese of Brazil
      (os.path.join('share', 'kana-no-quiz','locale','ru','LC_MESSAGES'),
         [os.path.join("data", "locale", "ru", "LC_MESSAGES",
         "kana-no-quiz.mo")]),  # Russian
      (os.path.join('share', 'kana-no-quiz','locale', 'sr', 'LC_MESSAGES'),
         [os.path.join("data", "locale", "sr", "LC_MESSAGES",
         "kana-no-quiz.mo")]),  # Serbian
      (os.path.join('share', 'kana-no-quiz', 'locale', 'sv', 'LC_MESSAGES'),
         [os.path.join("data", "locale", "sv", "LC_MESSAGES",
         "kana-no-quiz.mo")])]  # Swedish

if 'bdist_wininst' in sys.argv or 'py2exe' in sys.argv:
   # Windows Start Menu icon!
   datafiles.append((os.path.join("share", "kana-no-quiz", "img"),
      [os.path.join("data", "img", "icon.ico")]))

VERSION = '2.0 CVS'

setup(
   name      =   'Kana no quiz',
   version      =   VERSION,
   description   =   'A tool to memorize Japanese kana pronounciation.',
   long_description =   """
            Kana no quiz is a little educational tool, simple yet
            efficient, to memorize the pronunciation of Japanese
            kana (hiragana & katakana) in an quick, easy, and
            flexible fashion.
            
            This program features several ways and many options to
            either teach the complete beginner or test the wizard
            skill on kana recognition and pronouncing.
            
            Progressively, a great part of the Japanese writing
            (excepted Kanji) becomes phoneticaly readable to the
            foreign student, representing a first step into the
            learning of the language.

            """,
   author      =   'Choplair-network',
   author_email   =   'contact@choplair.org',
   url      =   'http://www.choplair.org/',
   download_url   =   'http://developer.berlios.de/project/filelist.php?group_id=1783',
   license      =   'GNU General Public License',
   packages   =   ['kananoquiz'],
   package_dir   =   {'kananoquiz': 'data/py'},
   scripts      =   scriptfiles,
   data_files   =   datafiles,
   # The following is for py2exe...
   windows    =   [{
            'script': os.path.join("data", "script",
               "kana-no-quiz_startup.pyw"),
            'icon_resources': [(1, os.path.join("data", "img",
               "icon.ico"))]
            }],
   options      =   {
            'py2exe': {
               'packages':'encodings',
               'includes': 'cairo, pango, pangocairo, atk, '\
                  'gobject, psyco, random, sets, gettext',
               "compressed": 1, "optimize": 1
            }}
   )

if "install" in sys.argv:
   # Post-installing stuffs (Unix).
   if os.name == "posix":
      print "Kana no quiz v%s has been successfully installed!\n"\
         "You may now use the 'kana-no-quiz' command to run the program." %
         VERSION
