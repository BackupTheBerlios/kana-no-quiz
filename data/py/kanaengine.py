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

class Usability:
	def __init__(self,sets,portions,kanalist):
		"""Creation of a list that tells which kana sets and portions
		are usable for quiz selection.

		List format : [SET LIST: [value telling if the first set is usable
		(1) or not (0), [PORTION LIST: values telling if the first set
		portion is usable (1) or not (0), etc.]], etc.]

		Given arguments to this function are a boolean list indicating
		sets usage and a number list indication set portion selected
		(0 for all or the number of the portion, which will have to
		be decremented)."""

		#Initialisation.
		self.usability = [[int(),list()],[int(),list()],[int(),list()],
		[int(),list()],[int(),list()],[int(),list()],[int(),list()]]

		#Filling of the list.
		i = 0
		for x in sets:
			#Tell whether the set is usable or not.
			if x=="true": self.usability[i][0] = 1
			else: self.usability[i][0] = 0

			#Tell whether the set portions are usable or not.
			if portions[i]==0: #All the portions are usable.
				for x in range(len(kanalist[i])):
					self.usability[i][1].append(1)
			else:  #Only one portion is usable.
				for x in range(len(kanalist[i])):
					if x==portions[i]-1: self.usability[i][1].append(1)
					else : self.usability[i][1].append(0)

			i+=1

	def getStateList(self,type):
		"""Creation of a simpler list containing only the state
		(usable or not) of each kana set (if type=0) or set
		portion (if type=1), then return of it."""

		list = []
		for x in range(7):
			list.append(self.usability[x][type])
		return list

class KanaEngine:
	def __init__(self):
		self.previous_kana = None
		self.default_kana_list = self.getKanaList()
		self.used_kana_list = self.getKanaList()

	def getKanaList(self):
		"""This function returns the kana full list, divided in 
		sets (the 3 first are hiragana, the nexts are katakana)
		then splited into small portions of 5/6 kana."""
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
		"""Randomly choose a kana, respecting many
		parameters, which will be the right answer."""

		if "true" in args[0]:
			#Definitions of some variables.
			portion_nums = args[1]
			self.no_repeat = args[2]

			ok = 0
			while not ok:
				#Althougth I know that's more ressource consuming to put this instruction in the while, 
				#it's buggy if it is placed just before (for reasons that I don't understand...). O_o
				#At least, it works ! But, anyway, this kana engine is hunted ! XD
				self.usability = Usability(args[0],args[1],self.getKanaList())

				sets = self.usability.getStateList(0)
				portions = self.usability.getStateList(1)

				for i in range(7):
					if sets[i]==1:
						#Set empty portion as unusable.
						for j in range(len(self.used_kana_list[i])):
							if self.used_kana_list[i][j]==[]:
								portions[i][j] = 0

						#Set the set as unusable if its only one used portion is also unusable.
						if portion_nums[i]!=0 and portions[i][portion_nums[i]-1]==0: sets[i] = 0

						#Set the set as unusable if its portions are all empty.
						if not 1 in portions[i]: sets[i] = 0

				#Selection of syllabary kind (hiragana=1 & katakana=0).
				if 1 in sets[0:3] and 1 in sets[3:7]: self.kind = random.choice((0,1)); ok = 1
				elif 1 in sets[0:3]: self.kind = 1; ok = 1
				elif 1 in sets[3:7]: self.kind = 0; ok = 1
				else: self.used_kana_list=self.getKanaList()

			#Selecton of possible question sets.
			possible_sets = []
			i = (3,0)[self.kind]
			for x in (sets[3:7],sets[0:3])[self.kind]:
				if x==1: possible_sets.append(i)
				i += 1

			#Selection of THE question set.
			if len(possible_sets)>1: self.set_num = random.choice(possible_sets)
			else: self.set_num = possible_sets[0]

			#Selection of the kana portion.
			if portion_nums[self.set_num]==0:
				i = []
				for x in range(len(self.used_kana_list[self.set_num])):
					if portions[self.set_num][x]==1: i.append(x)
				self.part_num = random.choice(i)
			else:
				self.part_num = portion_nums[self.set_num]-1
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
