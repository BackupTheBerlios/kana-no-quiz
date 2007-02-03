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

class PlaySound:
   def __init__(self, datarootpath, alsacardname):
      self.datarootpath = datarootpath
      self.alsacardname = alsacardname
      self.system = os.name

      # Using specific module for Unix / Windows platforms
      # (no Mac OS X support yet).
      if self.system == "posix":
         # Alsa audio output (using additional module).
         import alsaaudio
         try:
            self.out = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK,
               cardname="default")
         except alsaaudio.ALSAAudioError:
            print "Warning: unable to access ALSA playback device. "\
               "No sound will be heard."
            self.out = open(os.devnull, "w")
         else:
            self.out.setchannels(1)
            self.out.setrate(48000)
            self.out.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.out.setperiodsize(160)

      elif self.system == "nt":
         # Windows simple WAVE output (using Python built-in module)
         import winsound

   def play_kana(self, kana, gender):
      sound_path = os.path.join(self.datarootpath, "sound", "kana_%s"\
         % gender, "%s.wav" % kana)

      if os.path.isfile(sound_path):
         if self.system == "posix":
            file = open(sound_path, "r")
            i = 0
            while i < 42:
               data = file.read(320)
               self.out.write(data)
               i += 1
            file.close()
            return True

      else: return False

