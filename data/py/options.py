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

		#Default options & values.
		self.params  = {
		'basic_hiragana':'true',
		'basic_hiragana_part':0,
		'modified_hiragana':'false',
		'modified_hiragana_part':0,
		'contracted_hiragana':'false',
		'contracted_hiragana_part':0,
		'basic_katakana':'true',
		'basic_katakana_part':0,
		'modified_katakana':'false',
		'modified_katakana_part':0,
		'contracted_katakana':'false',
		'contracted_katakana_part':0,
		'additional_katakana':'false',
		'additional_katakana_part':0,
		'length':'normal',
		'answer_mode':'list',
		'list_size':'3'}
		if locale.getlocale() in ("fr","pt_BR","sv"): self.params['lang'] = locale.getlocale()
		else: self.params['lang'] = "en"

		#Valid values for each option contained as a tuple into a dictionnary.
		self.validValues = {
		'basic_hiragana':('true','false'),
		'basic_hiragana_part':range(10),
		'modified_hiragana':('true','false'),
		'modified_hiragana_part':range(5),
		'contracted_hiragana':('true','false'),
		'contracted_hiragana_part':range(5),
		'basic_katakana':('true','false'),
		'basic_katakana_part':range(10),
		'modified_katakana':('true','false'),
		'modified_katakana_part':range(5),
		'contracted_katakana':('true','false'),
		'contracted_katakana_part':range(5),
		'additional_katakana':('true','false'),
		'additional_katakana_part':range(5),
		'length':('short','normal','long'),
		'answer_mode':('list','entry'),
		'list_size':(2,3,4),
		'lang':('en','fr','pt_BR','sv')
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
					key,val = key.strip(),val.strip()
					if key in ('basic_hiragana_part','modified_hiragana_part',
						'contracted_hiragana_part','basic_katakana_part',
						'modified_katakana_part','contracted_katakana_part',
						'additional_katakana_part','list_size'): 
						try: val = int(val)
						except: pass
					self.check(key,val)
	
	def check(self,key,val):
		"""Here we check whether the option value, which has been read,
		is valid. In that case, the option value is modified. Otherwise, we
		keep the default value."""

		#Do valid values for this option have been referenced?
		if self.validValues.has_key(key):
			if val in self.validValues[key]: #The value is valid, so update the params.
				self.params[key] = val
		else:	#We use it, although it seems to be an unknow options.
			self.params[key] = val

	def val(self,name):
		if self.params.has_key(name): return self.params[name]
		else: return None

	def write(self,paramdict):
		#Configuration file header.
		content = """
# Kana no quiz configuration file.
# See `data/py/options.py' for more details. ;-)

"""
		#
		# Use of the amazing WAGLAMOT (tm) technology!
		#
		for key,val in paramdict.items():
			content += "%s %s\n" % (key,val) #Add to the output file content.
			self.params[key] = val #Update param dictionnary value.

		file = open(self.path,"wb") #Open (create if doesn't exist)
		file.write(content) #Write
		file.close() #And close

