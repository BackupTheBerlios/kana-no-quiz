"""
Kana no quiz!
Copyleft 2003, 2004 Choplair-network.

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
import os.path, locale

class Options:
	def __init__(self):
		self.path = "data/options.conf" #Set path to the configuration file.

		#Set default values.
		self.params  = {
		'single_katakana':'true',
		'modified_katakana':'false',
		'combined_katakana':'false',
		'single_hiragana':'true',
		'modified_hiragana':'false',
		'combined_hiragana':'false',
		'length':'normal',
		'difficulty':'medium'}
		if locale.getlocale() in ("fr","sv"): self.params['lang'] = locale.getlocale()
		else: self.params['lang'] = "en"

	def validValues(self):
		"""Valid values for each option are contained as a tuple into a dictionnary."""
		return {
		'single_katakana':('true','false'),
		'modified_katakana':('true','false'),
		'combined_katakana':('true','false'),
		'single_hiragana':('true','false'),
		'modified_hiragana':('true','false'),
		'combined_hiragana':('true','false'),
		'length':('short','normal','long'),
		'difficulty':('novice','medium','sensei'),
		'lang':('en','fr','sv')
		}

	def read(self):
		#Check whether the option file exists...
		if os.path.isfile(self.path):
			file = open(self.path,"r") #Open
			content = file.readlines() #Read the content.
			file.close() #And close :p

			for line in content:
				line.strip()
				if line[0]!="#" and line!="\n":
					key,val = split(line)
					self.check(key.strip(),val.strip())
	
	def check(self,key,val):
		"""Here we check whether the option value, which has been read,
		is valid. In that case option value is modified, otherwise we
		keep default value."""

		paramdict = self.validValues()
	
		#Do valid values for this option are referenced?
		if paramdict.has_key(key):
			if val in paramdict[key]: #The value is valid, so update the params.
				self.params[key] = val
		else:	#Although it seems to be an unknow options, we use it.
			self.params[key] = val

	def val(self,name):
		if self.params.has_key(name): return self.params[name]
		else: return None

	def write(self,paramdict):
		#Configuration file header.
		content = """
# Kana no quiz configuration file.
# Look at the source code for more details. ;-)

"""
		#
		# Use of the amazing WAGLAMOT (tm) technology!
		#
		for key,val in paramdict.items():
			content += "%s %s\n" % (key,val) #Add to the output file content.
			self.params[key] = val #Update param dictionnary value.

		file = open(self.path,"w") #Open (create if doesn't exist)
		file.write(content) #Write
		file.close() #And close
