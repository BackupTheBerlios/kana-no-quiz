"""
Kana no quiz!
Copyleft 2003, 2004, 2005 Choplair-network.

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
import random

class KanaEngine:
	def __init__(self):
		self.previous_kana = None
		self.default_kana_list,self.used_kana_list = self.getKanaList(),self.getKanaList()

	def getKanaList(self):
		"""This function returns the kana full list, divided in 
		sets then splited in small portions of 5/6 kana."""
		return (
		[ #Basic hiragana.
		["a",	"i",	"u",	"e",	"o"],
		["ka",	"ki",	"ku",	"ke",	"ko"],
		["sa",	"shi",	"su",	"se",	"so"],
		["ta",	"chi",	"tsu",	"te",	"to"],
		["na",	"ni",	"nu",	"ne",	"no"],
		["ha",	"hi",	"fu",	"he",	"ho"],
		["ma",	"mi",	"mu",	"me",	"mo"],
		["ra",	"ri",	"ru",	"re",	"ro"],
		["ya",		"yu",		"yo",
		"wa",					"o-2",
		"n"]],
		[ #Modified hiragana.
		["ga",	"gi",	"gu",	"ge",	"go"],
		["za",	"ji",	"zu",	"ze",	"zo"],
		["da",	"ji-2",	"zu-2",	"de",	"do"],
		["ba",	"bi",	"bu",	"be",	"bo"],
		["pa",	"pi",	"pu",	"pe",	"po"]],
		[ #Contracted hiragana.
		["kya",		"kyu",		"kyo",
		"gya",		"gyu",		"gyo"],
		["sha",		"shu",		"sho",
		"ja",		"ju",		"jo"],
		["cha",		"chu",		"cho",
		"nya",		"nyu",		"nyo"],
		["rya",		"ryu",		"ryo",
		"hya",		"hyu",		"hyo"],
		["bya",		"byu",		"byo",
		"pya",		"pyu",		"pyo"]],
		[ #Basic katakana.
		["a",	"i",	"u",	"e",	"o"],
		["ka",	"ki",	"ku",	"ke",	"ko"],
		["sa",	"shi",	"su",	"se",	"so"],
		["ta",	"chi",	"tsu",	"te",	"to"],
		["na",	"ni",	"nu",	"ne",	"no"],
		["ha",	"hi",	"fu",	"he",	"ho"],
		["ma",	"mi",	"mu",	"me",	"mo"],
		["ra",	"ri",	"ru",	"re",	"ro"],
		["ya",		"yu",		"yo",
		"wa",					"o-2",
		"n"]],
		[ #Modified katakana.
		["ga",	"gi",	"gu",	"ge",	"go"],
		["za",	"ji",	"zu",	"ze",	"zo"],
		["da",	"ji-2",	"zu-2",	"de",	"do"],
		["ba",	"bi",	"bu",	"be",	"bo"],
		["pa",	"pi",	"pu",	"pe",	"po"]],
		[ #Contracted katakana.
		["kya",		"kyu",		"kyo",
		"gya",		"gyu",		"gyo"],
		["sha",		"shu",		"sho",
		"ja",		"ju",		"jo"],
		["cha",		"chu",		"cho",
		"nya",		"nyu",		"nyo"],
		["rya",		"ryu",		"ryo",
		"hya",		"hyu",		"hyo"],
		["bya",		"byu",		"byo",
		"pya",		"pyu",		"pyo"]],
		[ #Additional katakana.
		[	"wi",		"we",	"wo",
		"kwa",				"kwo",
		"gwa"],
		[			"she",
					"je",
					"che",
		"tsa",			"tse",	"tso"],
		[	"ti",	"tu",
			"di",	"du",
			"tyu",	"dyu"],
		[			"ye",
		"fa",	"fi",		"fe",	"fo"],
		["va",	"vi",	"vu",	"ve",	"vo"]])

	def randomKana(self,*args):
		if "true" in args[0]:
			ok = 0
			while not ok:
				sets = list(args[0])
				self.parts = args[1]
				self.no_repeat = args[2]
	
				for i in range(7):
					if sets[i]=="true":
						#Disable set when the only part used is empty.
						if self.parts[i]!=0 and self.used_kana_list[i][self.parts[i]-1]==[]:
							sets[i] = "false"

						#Remove empty part.
						if self.parts[i]==0:
							for j in self.used_kana_list[i]:
								if j==[]: self.used_kana_list[i].remove(j)
						#Disable empty set.
						if self.used_kana_list[i]==[]: sets[i] = "false"

				#Selection of syllabary kind.
				if "true" in sets[0:3] and "true" in sets[3:7]: self.kind = random.choice((0,1)); ok = 1
				elif "true" in sets[0:3]: self.kind = 1; ok = 1
				elif "true" in sets[3:7]: self.kind = 0; ok = 1
				else: self.used_kana_list=self.getKanaList(); continue

			#Selecton of possible question sets.
			possible_sets = []
			i = (3,0)[self.kind]
			for value in (sets[3:7],sets[0:3])[self.kind]:
				if value=="true": possible_sets.append(i)
				i += 1

			#Selection of THE question set.
			if len(possible_sets)>1: self.set_num = random.choice(possible_sets)
			else: self.set_num = possible_sets[0]

			#Selection of the kana part.
			if self.parts[self.set_num]==0:
				self.part_num = random.choice(range(len(self.used_kana_list[self.set_num])))
			else:
				self.part_num = self.parts[self.set_num]-1
			self.part = self.used_kana_list[self.set_num][self.part_num]
	
			#Selection of the kana.
			self.kana = random.choice(self.part)
			while self.kana==self.previous_kana:
				#Prevention of selecting the same kana than previously.
				self.kana = random.choice(self.part)

			if self.no_repeat=="true":
				#The no-repeat option is activated, so we remove the kana from the list to prevent future selection.
				self.used_kana_list[self.set_num][self.part_num].remove(self.kana)

			#Precisely memorize this kana to prevent it to be selected the next time.
			self.previous_kana = self.kana

			return self.kana

		else: return 0

	def getKanaKind(self): return self.kind #Katakana = 0 & hiragana = 1.

	def getASet(self,num):
		"""Return a set from its number."""
		return self.default_kana_list[num]

	def randomAnswers(self,list_size):
		#Anwsers will be get from this temporary question set, it is the same kana part than the selected kana.
		templist = self.getKanaList()[self.set_num][self.part_num]
		answers = [] #Anwsers' list.

		#First, addition of the selected kana in the list of answer.
		answers.append(self.kana)
		#Remove the selected kana from the temporary answer list to prevent a double selection as an answer.
		templist.remove(self.kana)

		for x in range(int(list_size)-1):
			x = random.choice(templist) #Take a random wrong anwsers from the kana list.

			#Prevent selection of kana with the same romanji transcription.
			if x[-2:]=="-2" and x[:-2] in templist: templist.remove(x[:-2])
			elif "%s-2" % x in templist: templist.remove("%s-2" % x)

			answers.append(x)
			templist.remove(x) #We remove it from the kana list to prevent multiple selection of the same kana...

		random.shuffle(answers)

		return answers
