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
from string import split
import os, locale
import kanaengine

class Options:
   def __init__(self, conf_dir = "~/.kana-no-quiz"):
      # Kana no quiz local configuration directory.
      self.conf_dir = os.path.expanduser(conf_dir)
      # Path to the configuration file.
      self.conf_file = os.path.join(self.conf_dir, "option.conf") 

      self.params = {}
      # Valid values for each restricted option, contained as a tuple into a
      # dictionnary.
      self.validValues = {
      'basic_hiragana': ('true','false'),
      'modified_hiragana': ('true','false'),
      'contracted_hiragana': ('true','false'),
      'basic_katakana': ('true','false'),
      'modified_katakana': ('true','false'),
      'contracted_katakana': ('true','false'),
      'additional_katakana': ('true','false'),
      'allow_repetition': ('true', 'false'),
      'transcription_system': kanaengine.transcriptions,
      'answering_mode': ('list','entry'),
      'list_size': range(2, 6),
      'rand_answer_sel_range': ('portion','set','kind'),
      'kana_no_repeat': ('true','false'),
      'lang': ('de', 'en', 'es', 'fr', 'gl', 'pt_BR', 'ru', 'sr',
        'sv'),
      'kana_image_theme': ('choplair', 'kanatest'),
      'kana_image_scale': ('small', 'medium', 'large'),
      'answer_display_timeout': range(4),
      'kana_pronouncing': ('female', 'male', 'alternate')
      }
      self.set_default_values()

   # This is separated so I can test it independently
   def set_default_values(self):
      # Default options & values.
      defaults = {
      'basic_hiragana': 'true',
      'basic_hiragana_portions': (1, 1,1, 1,1, 1,1, 1,1),
      'modified_hiragana': 'false',
      'modified_hiragana_portions': (1, 1,1, 1,1),
      'contracted_hiragana': 'false',
      'contracted_hiragana_portions': (1, 1,1, 1,1),
      'basic_katakana': 'true',
      'basic_katakana_portions': (1, 1,1, 1,1, 1,1, 1,1),
      'modified_katakana': 'false',
      'modified_katakana_portions': (1, 1,1, 1,1),
      'contracted_katakana': 'false',
      'contracted_katakana_portions': (1, 1,1, 1,1),
      'additional_katakana': 'false',
      'additional_katakana_portions': (1, 1,1, 1,1),
      'transcription_system': 'hepburn',
      'allow_repetition': 'false',
      'length': 20,
      'kana_no_repeat': 'false',
      'answering_mode': 'list',
      'list_size': 3,
      'rand_answer_sel_range': 'portion',
      'kana_image_theme': 'choplair',
      'kana_image_scale': 'medium',
      'answer_display_timeout': 0,
      'kana_pronouncing': 'alternate'
      }
      if locale.getlocale() in ("de", "es", "fr", "gl", "pt_BR",
        "ru", "sr", "sv"):
         self.params['lang'] = locale.getlocale()
      else: self.params['lang'] = "en"

      for key, value in defaults.iteritems():
         self[key] = value

   def read_from_file(self):
      # Checking whether the option file exists...
      if os.path.isfile(self.conf_file):
         file = open(self.conf_file, "r") # Opening.
         content = file.readlines() # Reading the content.
         file.close() # And closing. :p

         self.parse_options(content)

   def parse_options(self, content):
      for line in content:
         line.strip()
         # Comments and blank lines are skipped.
         if line[0] != "#" and line != "\n":
            bouyaka = split(line)
            # The first word is the option name.
            key = bouyaka[0]
            # Value may contains spaces.
            val = ""
            for x in bouyaka[1:]:
               val += "%s " % x
            val = val.strip()
            
            # String to integrer list convertion (kana portions).
            if key[-8:] == "portions":
               plop = list()
               for x in val.split(","): plop.append(int(x))
               val = plop

            self[key] = val

   # This integrates setting and checking into one move
   def __setitem__(self, key, val):
      """Here we check whether the option value, which has been read,
         is valid. In that case, the option value is modified. Otherwise, we
         keep the default value.
      
      """
      # Is it an option with restricted values?
      if self.validValues.has_key(key):
         if val in self.validValues[key]:
            # The value is valid, so update the param.
            self.params[key] = val
         else:
            try: 
               if int(val) in self.validValues[key]:
                  # As an integrer, the value is valid, so update the param.
                  self.params[key] = int(val)
               else:
                  raise ValueError("Illegal value for %s: %s"   %
                     (key, val))
            except:
               raise ValueError("Illegal value for %s: %s." % (key, val))
      else:
         # Not taking care of the value since it is not a restricted option.
         self.params[key] = val

      # Special processing: Is this a 'portion'?
      if key[-9:] == '_portions':
         self.set_portion(key, val)
         return

      # Special processing: Is this the name of a kind?
      try:
         kanaSet = kanaengine.kanaSetByOptionKey[key]
         kanaSet.active = val == "true"
      except KeyError:
         pass

   def set_portion(self, key, value):
      """self.set_portion('basic_hiragana_portion', [1, 1, 0, ...]

         Sets the .active on the appropriate Kana portions.

      """
      kanaSet = kanaengine.kanaSetByOptionKey[key[:-9]]
      for portion, value in zip(kanaSet.portions, value):
         portion.active = value
         
   def __getitem__(self,key):
      # This guarantees the .active flag and the config will be
      # in sync.
      if key[-9:] == "_portions":
         # Extract it from the live kana data
         kanaSet = kanaengine.kanaSetByOptionKey[key[:-9]]
         return tuple([x.active + 0 for x in kanaSet.portions])
      
      return self.params[key]

   def __iter__(self):
      return iter(self.params)
   def iterkeys(self):
      return iter(self.params)
   def iteritems(self):
      return self.params.iteritems()

   def write(self):
      # Configuration file header.
      content = "# Kana no quiz configuration file.\n\n"

      for key, val in self.iteritems():
         self[key] = val

      #
      # Use of the amazing WAGLAMOT (tm) technology!
      #
      for key, val in self.iteritems():
         # The param values written to the configuration files may slightly
         # differ from their interal format. So there is a second variable
         # just for configuration file output.
         written_val = val

         # List to string convertion (kana portions).
         if key[-8:] == "portions": 
            string = str()
            for x in written_val: string += "%s," % x
            written_val = string[:-1]

         # Adding to the output file content.
         content += "%s %s\n" % (key, written_val)

      if not os.path.isdir(self.conf_dir):
         # Creating Kana no quiz configuration directory.
         os.mkdir(self.conf_dir)

      # Writing configuration file...
      file = open(self.conf_file, "wb") 
      file.write(content) 
      file.close() 
 
