"""Kana no quiz!
   Copyleft 2007 Choplair-network.
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
from pygame import mixer

class PlaySound:
   """Cross platform Kana sound playing, using the PyGame library."""
   def __init__(self, datarootpath):
      self.datarootpath = datarootpath
      mixer.init(48000)  # Initializing mixer, at 48kHz.

   def play_kana(self, kana, gender):
      sound_path = os.path.join(self.datarootpath, "sound", "kana_%s"\
         % gender, "%s.wav" % kana)

      if os.path.isfile(sound_path):
        mixer.Sound(sound_path).play()
        return True
      else: return False
