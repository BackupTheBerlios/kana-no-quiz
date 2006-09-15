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
from string import split
import os, locale
import kanaengine
import re

# Later, we'll want to eliminate these functions by matching the names
# in both places
def optionToKindName(optionName):
	"""This converts the option name ('basic_hiragana_portion') into
	the name of the kana kind ('Basic Hiragana'), so we can retrieve
	the correct Kind from kanaengine."""

	# Peel off the "_portion" if we have it
	if optionName[-9:] == "_portions":
		optionName = optionName[:-9]
	optionName = optionName.split("_")

	optionName = [x[0].upper() + x[1:] for x in optionName]
	return " ".join(optionName)

def kindNameToOption(kindName):
	pieces = kindName.split(" ")
	pieces = [x.lower() for x in pieces]
	return "_".join(pieces)

class Options:
	def __init__(self, conf_dir = "~/.kana-no-quiz"):
		self.conf_dir = os.path.expanduser(conf_dir) #Kana no quiz local configuration directory.
		self.conf_file = os.path.join(self.conf_dir,"option.conf")  #Set path to the configuration file.

		self.params = {}
		#Valid values for each option contained as a tuple into a dictionnary.
		self.validValues = {
		'basic_hiragana':('true','false'),
		'modified_hiragana':('true','false'),
		'contracted_hiragana':('true','false'),
		'basic_katakana':('true','false'),
		'modified_katakana':('true','false'),
		'contracted_katakana':('true','false'),
		'additional_katakana':('true','false'),
		'allow_repetition':('true', 'false'),
		'transcription_system':kanaengine.transcriptions,
		'answer_mode':('list','entry'),
		'list_size':(2,3,4,5),
		'rand_answer_sel_range':('portion','set','kind'),
		'kana_no_repeat':('true','false'),
		'lang':('de','en','fr','pt_BR','ru','sr','sv')
		}
		self.setDefaultValues()

	# This is separated so I can test it independently
	def setDefaultValues(self):
		#Default options & values.
		defaults = {
		'basic_hiragana':'true',
		'basic_hiragana_portions':(1,1,1,1,1,1,1,1,1),
		'modified_hiragana':'false',
		'modified_hiragana_portions':(1,1,1,1,1),
		'contracted_hiragana':'false',
		'contracted_hiragana_portions':(1,1,1,1,1),
		'basic_katakana':'true',
		'basic_katakana_portions':(1,1,1,1,1,1,1,1,1),
		'modified_katakana':'false',
		'modified_katakana_portions':(1,1,1,1,1),
		'contracted_katakana':'false',
		'contracted_katakana_portions':(1,1,1,1,1),
		'additional_katakana':'false',
		'additional_katakana_portions':(1,1,1,1,1),
		'transcription_system':'hepburn',
		'allow_repetition': 'false',
		'length':20,
		'kana_no_repeat':'false',
		'answer_mode':'list',
		'list_size':3,
		'rand_answer_sel_range':'portion'}
		if locale.getlocale() in ("de","fr","pt_BR","ru","sr","sv"): self.params['lang'] = locale.getlocale()
		else: self.params['lang'] = "en"

		for key, value in defaults.iteritems():
			self[key] = value

	def read(self):
		#Check whether the option file exists...
		if os.path.isfile(self.conf_file):
			file = open(self.conf_file,"r") #Open.
			content = file.readlines() #Read the content.
			file.close() #And close. :p

			for line in content:
				line.strip()
				if line[0]!="#" and line!="\n":
					key,val = split(line)[:2]
					key,val = key.strip(),val.strip()

					#String to integrer list convertion (kana portions).
					if key[-8:]=="portions":
						plop = list()
						for x in val.split(","): plop.append(int(x))
						val = plop

					self[key] = val

    # This integrates setting and checking into one move
	def __setitem__(self,key,val):
		"""Here we check whether the option value, which has been read,
		is valid. In that case, the option value is modified. Otherwise, we
		keep the default value."""

		#Do valid values for this option have been referenced?
		if self.validValues.has_key(key):
			if val in self.validValues[key]:
				#The value is valid, so update the param.
				self.params[key] = val
			else:
				try: 
					if int(val) in self.validValues[key]:
						#As an integrer, the value is valid, so update the param.
						self.params[key] = int(val)
					else:
						raise ValueError("Illegal value for %s: %s"
										 %(key, val))
				except:
					raise ValueError("Illegal value for %s: %s."
									 %(key, val))
		else:
			#We use it, although it seems to be an unknown option.
			self.params[key] = val

		# Special processing: Is this a 'portion'?
		if key[-9:] == '_portions':
			self.setPortion(key, val)
			return

		# Special processing: Is this the name of a kind?
		kanaKind = optionToKindName(key)
		try:
			kanaSet = kanaengine.kanaSetByName[kanaKind]
			kanaSet.active = val == "true"
		except KeyError:
			pass

	def setPortion(self, key, value):
		"""self.setPortion('basic_hiragana_portion', [1, 1, 0, ...]

		Sets the .active on the appropriate Kana portions."""
		portionName = optionToKindName(key)
		kanaSet = kanaengine.kanaSetByName[portionName]
		for portion, value in zip(kanaSet.portions, value):
			portion.active = value
            
	def __getitem__(self,name):
		# Generally it's better to pass the KeyError along.
		return self.params[name]

	def __iter__(self):
		return iter(self.params)
	def iterkeys(self):
		return iter(self.params)
	def iteritems(self):
		return self.params.iteritems()

	def write(self,paramdict):
		#Configuration file header.
		content = "# Kana no quiz configuration file.\n\n"

		for key, val in paramdict.iteritems():
			self[key] = val

		#
		# Use of the amazing WAGLAMOT (tm) technology!
		#
		for key,val in self.iteritems():
			#The param values written to the configuration files may slightly differ from their interal format.
			#So there is a second variable just for configuration file output.
		
			written_val = val

			#List to string convertion (kana portions).
			if key[-8:]=="portions": 
				string = str()
				for x in written_val: string += "%s," % x
				written_val = string[:-1]

			content += "%s %s\n" % (key,written_val) #Add to the output file content.

		if not os.path.isdir(self.conf_dir): os.mkdir(self.conf_dir)  #Create user config directory if doesn't exist.
		file = open(self.conf_file,"wb") #Open (create if doesn't exist)
		file.write(content) #Write
		file.close() #And close
