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
import random

if os.name == "nt": # Using Python built-in module for Windows.
   import winsound
else: # Using Pygame for other OSs.
   from pygame import mixer

class PlaySound:
   """Cross platform Kana sound playing, using the PyGame library (and
   the Winsound one for Windows)."""
   def __init__(self, datarootpath):
      self.datarootpath = datarootpath
      self.past_gender = "male"  # Ladies first.
    
      if not os.name == "nt":
         mixer.init(48000)  # Initializing Pygame mixer, at 48kHz.

   def play_kana(self, kana, gender):
      if gender == "alternate":
         if self.past_gender == "female":
            self.past_gender, gender = "male", "male"
         else:
            self.past_gender, gender = "female", "female"

      sound_path = os.path.join(self.datarootpath, "sound", "kana_%s"\
         % gender, "%s.wav" % kana)

      if not os.path.isfile(sound_path):
        return False
      elif os.name == "nt": # Using Python built-in module for Windows.
         winsound.PlaySound(sound_path, winsound.SND_FILENAME | \
            winsound.SND_ASYNC)
      else: # Using Pygame for other OSs.
         if os.path.isfile(sound_path):
           mixer.Sound(sound_path).play()
           return True


