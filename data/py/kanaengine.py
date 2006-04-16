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
import random

class Usability:
	def __init__(self,sets,portions):
		"""Creation of a list that tells which kana sets and portions
		are usable for quiz selection.

		List format : [SET LIST: [value telling if the first set is usable
		(1) or not (0), [PORTION LIST: values telling if the first set
		portion is usable (1) or not (0), etc.]], etc.]

		Given arguments to this function are a boolean list indicating
		sets usage and a list indicating which set portion enabled (1)
		or not (0)."""

		#Initialisation.
		self.usability = [[int(),list()],[int(),list()],[int(),list()],
		[int(),list()],[int(),list()],[int(),list()],[int(),list()]]

		#Filling of the list.
		i = 0
		for x in sets:
			#Tell whether the set is enabled or not.
			self.usability[i][0] = (0,1)[x=="true"] 
			#Tell whether the set portions are enabled or not.
			for x in portions[i]: self.usability[i][1].append(x)
			i+=1

	def getStateList(self,type):
		"""Creation of a simpler list containing only the state
		(usable or not) of each kana set (if type=0) or set
		portions (if type=1), then returning it."""

		plop = []
		for x in range(7):
			plop.append(self.usability[x][type])
		return plop

def HepburnToOtherSysConvert(kana,outputsys):
	#Kunrei-shiki/Nihon-shiki common kana values.
	if outputsys in ("kunrei-shiki","nihon-shiki"):
		convert = {
			"shi":"si", "sha":"sya", "shu":"syu", "sho":"syo",
			"ji":"zi", "ja":"zya", "ju":"zyu", "jo":"zyo",
			"tsu":"tu", "chi":"ti", "cha":"tya", "chu":"tyu",
			"cho":"tyo", "fu":"hu"}
		if convert.has_key(kana): return convert[kana]

		#Kunrei-shiki specific kana values.
		if outputsys=="kunrei-shiki":
			if kana=="ji-2": return "zi" 
		#Nihon-shiki specific kana values.
		elif outputsys=="nihon-shiki":
			if kana=="ji-2": return "di"
			elif kana=="zu-2": return "du"

	#Convertion to Polivanov.	
	if outputsys=="polivanov":
		convert = {
			#Basic/modified kana.
			"a":"а", "i":"и", "u":"у", "e":"э", "o":"о",
			"ka":"ка", "ki":"ки", "ku":"ку","ke":"кэ", "ko":"ко",
			"ga":"га", "gi":"ги", "gu":"гу", "ge":"гэ", "go":"го",
			"sa": "са", "shi":"си", "su":"су", "se":"сэ", "so":"со",
			"za":"дза", "ji":"дзи", "zu":"дзу", "ze": "дзэ", "zo":"дзо",
			"ta":"та", "chi":"ти", "tsu":"цу", "te":"тэ", "to":"то",
			"da":"да", "ji":"дзи", "zu":"дзу", "de":"дэ", "do": "до",
			"na":"на", "ni":"ни", "nu":"ну", "ne":"нэ", "no":"но",
			"ha":"ха", "hi":"хи", "fu":"фу",  "he":"хэ", "ho":"хо",
			"pa":"па", "pi":"пи", "pu":"пу", "pe":"пэ", "po":"по",
			"ba":"ба", "bi":"би", "bu":"бу", "be":"бэ", "bo":"бо",
			"ma":"ма", "mi":"ми", "mu":"му", "me":"мэ", "mo":"мо",
			"ya":"я", "yu":"ю", "yo":"ё",
			"ra":"ра", "ri":"ри", "ru":"ру", "re":"рэ", "ro":"ро",
			"wa":"ва", "o-2":"о", "n":"н", 
			#Contracted kana.
			"kya":"кя", "kyu":"кю", "kyo":"кё",
			"gya":"гя", "gyu":"гю", "gyo":"гё",
			"sha":"ся", "shu":"сю",	"sho":"сё",
			"ja":"дзя", "ju":"дзю", "jo":"дзё",
			"cha":"тя", "chu":"тю",	"cho":"тё",
			"ja":"дзя", "ju":"дзю", "jo":"дзё",
			"nya":"ня", "nyu":"ню", "nyo":"нё",
			"hya":"хя", "hyu":"хю", "hyo":"хё",
			"pya":"пя", "pyu":"пю", "pyo":"пё",
			"bya":"бя", "byu":"бю", "byo":"бё",
			"mya":"мя", "myu":"мю", "myo":"мё",
			"rya":"ря", "ryu":"рю", "ryo":"рё",
			#Additionnal katakana.
			"wi":"вх", "we":"вщ", "wo":"вн",
			"kwa":"ква", "kwo":"квн",
			"she":"сэ", "je":"дзщ", "che":"тэ",
			"tsa":"цю", "tse":"цщ", "tso":"цн",
			"ti":"ти", "tu":"ту", "di":"ди", "du":"ду",
			"tyu":"тю", "dyu":"дю", "ye":"е",
			"fa":"тю", "fi":"тх", "fe":"тщ", "fo":"тн",
			"va":"вю","vi":"вх","ve":"вщ","vo":"вн"}
		if convert.has_key(kana): return convert[kana]

	#Return the same value if no modification of the kana beetween the systems.
	return kana

class KanaEngine:
	def __init__(self):
		self.previous_kana = None
		self.default_kana_list = self.getKanaList()
		self.used_kana_list = self.getKanaList()
		
	def reset(self):
		"""Reset main variable values (i.e. when quiz	is finished,
		to permit starting one another	in a safe mode)."""
		self.__init__()

	def getKanaList(self):
		"""This function returns the kana full list (using default/
		Hepburn	trascription), divided in sets (the 3 firsts are
		hiragana, the 4 nexts are katakana) then splited into small
		portions	of 5/6 kana."""
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
		"wa",				"o-2",
		"n"]],
		[ #Modified hiragana.
		["ga",	"gi",	"gu",	"ge",	"go"],
		["za",	"ji",	"zu",	"ze",	"zo"],
		["da",	"ji-2","zu-2",	"de",	"do"],
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
		"wa",				"o-2",
		"n"]],
		[ #Modified katakana.
		["ga",	"gi",	"gu",	"ge",	"go"],
		["za",	"ji",	"zu",	"ze",	"zo"],
		["da",	"ji-2","zu-2",	"de",	"do"],
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

	def kanaSelectParams(self,*args):
		"""Kana will be choosed respecting these
		parameters."""
		self.select_params = args

	def randomKana(self):
		"""Randomly choose a kana which will be
		considered as the right answer."""

		if "true" in self.select_params[0]:
			ok = 0
			while not ok:
				#Althougth I know that's more ressource consuming to put this instruction in the ``while", 
				#it becomes buggy when placed just before (for reasons which I don't understand...). O_o
				#At least, it works! But, anyway, this kana engine is hunted! XD
				self.usability = Usability(self.select_params[0],self.select_params[1])

				sets = self.usability.getStateList(0)
				portions = self.usability.getStateList(1)

				for i in range(7):
					if sets[i]==1:
						#Disable empty portion.
						for j in range(len(self.used_kana_list[i])):
							if self.used_kana_list[i][j]==[]:
								portions[i][j] = 0

						#Disable set if it only contains disabled portions.
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
			plop = []; i = 0
			for x in portions[self.set_num]:
				if x==1: plop.append(i)
				i+=1
			self.portion_num = random.choice(plop)
			self.portion = self.used_kana_list[self.set_num][self.portion_num]

			#Selection of the kana.
			self.kana = random.choice(self.portion)
			while self.kana==self.previous_kana:
				#Prevention of selecting the same kana than previously.
				self.kana = random.choice(self.portion)

			if self.select_params[2]=="true":
				#The no-repeat option is activated, so we remove the kana from the list to prevent future selection.
				self.used_kana_list[self.set_num][self.portion_num].remove(self.kana)
				print len(self.used_kana_list[0][0])

			#Precisely memorize this kana to prevent it to be selected the next time.
			self.previous_kana = self.kana
			
			return self.kana

		else: return False

	def getKanaKind(self): return self.kind #Katakana = 0 & hiragana = 1.

	def getASet(self,num):
		"""Return a set from its number."""
		return self.default_kana_list[num]

	def randomAnswers(self,list_size):
		#Anwsers will be get from this temporary question set, it is the same kana portion than the selected kana.
		templist = self.getKanaList()[self.set_num][self.portion_num]
		answers = [] #Anwsers' list.

		#First, addition of the selected kana in the list of answer.
		answers.append(self.kana)
		#Remove the selected kana from the temporary answer list to prevent a double selection as an answer.
		templist.remove(self.kana)

		for x in range(int(list_size)-1):
			x = random.choice(templist) #Take a random wrong anwsers from the kana list.

			#Prevent selection of kana with the same romaji transcription.
			if x[-2:]=="-2" and x[:-2] in templist: templist.remove(x[:-2])
			elif "%s-2" % x in templist: templist.remove("%s-2" % x)

			answers.append(x)
			templist.remove(x) #We remove it from the kana list to prevent multiple selection of the same kana...

		random.shuffle(answers)

		return answers
