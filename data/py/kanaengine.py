# -*- coding: utf8 -*-
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
from sets import Set

transcriptions = ('hepburn','kunrei-shiki','nihon-shiki','polivanov')

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
			"nya":"ня", "nyu":"ню", "nyo":"нё",
			"hya":"хя", "hyu":"хю", "hyo":"хё",
			"pya":"пя", "pyu":"пю", "pyo":"пё",
			"bya":"бя", "byu":"бю", "byo":"бё",
			"mya":"мя", "myu":"мю", "myo":"мё",
			"rya":"ря", "ryu":"рю", "ryo":"рё",
			#Additionnal katakana.
			"wi":"ви", "we":"вэ", "wo":"во",
			"kwa":"ква", "kwo":"кво",
			"she":"се", "je":"дзэ", "che":"тэ",
			"tsa":"ца", "tse":"цэ", "tso":"цо",
			"ti":"ти", "tu":"ту", "di":"ди", "du":"ду",
			"tyu":"тю", "dyu":"дю", "ye":"е",
			"fa":"фа", "fi":"фи", "fe":"фэ", "fo":"фо",
			"va":"ва","vi":"ви","ve":"вэ","vo":"во"}
		if convert.has_key(kana): return convert[kana]

	#Return the same value if no modification of the kana beetween the systems.
	return kana

class KanaEngine:
	def __init__(self):
		self.reset()
		
	def reset(self):
		"""Reset main variable values (i.e. when quiz	is finished,
		to permit starting one another	in a safe mode)."""
		self.previous_kana = None
		self.default_kana_list = self.getKanaList()
		self.used_kana_set = set()

	def getKanaList(self):
		"""This function returns the kana full list (using default/
	            content = [x for x in content if 	Hepburn	trascription), divided in sets (the 3 firsts are
		hiragana, the 4 nexts are katakana) then splited into small
		portions	of 5/6 kana."""
		return kanaList

	def kanaSelectParams(self,*args):
		"""Kana will be choosed respecting these
		parameters."""
		self.select_params = {
			# "set_states":args[0], # now set up elsewhere
			# "portion_states":args[1], also set up elsewhere
			"allow_repetition":args[2],
			"rand_answer_sel_range":args[3]}

	def randomKana(self):
		"""Randomly choose a kana which will be
		considered as the right answer."""

		possibleKanaSet = set()
		hiragana.getActiveKana(possibleKanaSet)
		katakana.getActiveKana(possibleKanaSet)

		# Eliminate the previous kana
		if self.previous_kana in possibleKanaSet:
			possibleKanaSet.remove(self.previous_kana)

		# Isn't the sense of this clause backwards?
		blockRepetition = self.select_params['allow_repetition'] == 'true'

		# If we're not allowing repeats...
		if blockRepetition:
			# and there will actually be something left when
			# we remove all previously-used kana
			if possibleKanaSet > self.used_kana_set:
				# then remove the used kana
				possibleKanaSet.difference_update(self.used_kana_set)
			else:
				# there would be nothing left, so reset the used set
				# and ignore it for now
				self.used_kana_set = set()

		# uh oh, everything's been eliminated! really shouldn't happen.
		if not possibleKanaSet:
			return False

		chosenKana = random.choice(list(possibleKanaSet))

		self.previous_kana = chosenKana

		self.kana = chosenKana

		if blockRepetition:
			self.used_kana_set.add(chosenKana)

		return chosenKana

	def randomAnswers(self, list_size, kana = None):
		"""Selection of random wrong anwsers from a certain range, mixed
		with the previously selected ("right") kana into a list which gets shuffled
		and is returned at the end of this function."""

		# The answers that will be returned
		if kana is not None:
			answer = kana
		else:
			answer = self.kana
		answers = set()

		selectionRange = self.select_params['rand_answer_sel_range']

		possibleAnswers = set()

		# Get the portion, kind, or set of possible kana answers;
		# translates to something like
		# 'answer.portion.getActiveKana(possibleAnswers)
		getattr(answer, selectionRange).getActiveKana(possibleAnswers)

		# Remove the correct answer if it's there, to prevent
		# duplication
		possibleAnswers.discard(answer)

		for x in range(int(list_size)-1):
			wrongAnswer = random.choice(list(possibleAnswers))

			# Don't pick it again
			possibleAnswers.remove(wrongAnswer)
			
			answers.add(wrongAnswer)

		# Put the correct answer in
		answers.add(answer)
		answerList = list(answers)
		# Shuffling the answer list before returning it.
		random.shuffle(answerList)

		return answerList

kanaList = {'Basic hiragana': [
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
		'Modified hiragana':
		[
		["ga",	"gi",	"gu",	"ge",	"go"],
		["za",	"ji",	"zu",	"ze",	"zo"],
		["da",	"ji-2","zu-2",	"de",	"do"],
		["ba",	"bi",	"bu",	"be",	"bo"],
		["pa",	"pi",	"pu",	"pe",	"po"]],
		'Contracted hiragana':
		[
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
		'Basic katakana':
		[
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
		'Modified katakana':	
		[
		["ga",	"gi",	"gu",	"ge",	"go"],
		["za",	"ji",	"zu",	"ze",	"zo"],
		["da",	"ji-2","zu-2",	"de",	"do"],
		["ba",	"bi",	"bu",	"be",	"bo"],
		["pa",	"pi",	"pu",	"pe",	"po"]],
		'Contracted katakana':
		[
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
		'Additional katakana':
		[
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
		["va",	"vi",	"vu",	"ve",	"vo"]]}

order = ('Basic hiragana', 'Modified hiragana', 'Contracted hiragana',
		 'Basic katakana', 'Modified katakana', 'Contracted katakana',
		 'Additional katakana')

class KanaKind(object):
	"""Represents a kind of Kana, one of the alphabets."""
	def __init__(self, kind, kindIndex):
		self.kind = kind
		self.members = {}
		self.sets = {}
		self.setOrder = []
		self.kindIndex = kindIndex

	# Allow setting membership via katakana['shi'] = Kana(shi, ...)
	def __setitem__(self, key, value):
		self.members[key] = value
	def __getitem__(self, key):
		return self.members[key]

	def getActiveKana(self, answerSet = None):
		if answerSet is None:
			answerSet = set()
			
		for kanaSet in self.sets.values():
			kanaSet.getActiveKana(answerSet)

		return answerSet

	def setsInOrder(self):
		sets = []
		for setName in self.setOrder:
			sets.append(self.sets[setName])
		return sets

	def getSet(self, setName):
		try:
			return self.sets[setName]
		except KeyError:
			set = KanaSet(setName, self)
			self.setOrder.append(setName)
			self.sets[setName] = set
			return set

hiragana = KanaKind('hiragana', 1)
katakana = KanaKind('katakana', 0)
kanaKinds = {'hiragana': hiragana,
			 'katakana': katakana}

# Currently, the order matches the set specifications; as we move
# away from that, we'll get to just kanaSetByName
kanaSets = []
kanaSetByName = {}

# This should not be needed
setNameToMsg = {
	"Basic": 23,
	"Modified": 24,
	"Contracted": 25,
	"Additional": 26
	}


class KanaSet(object):
	"""Represents a question set of kana (basic, modified, contracted,
	etc."""
	def __init__(self, setName, kind):
		self.setName = setName
		self.kana = Set()
		self.portions = []
		self.active = 0
		self.kind = kind

		self.optionKey = setName.lower() + "_" + kind.kind
		self.imageName = self.optionKey + ".gif"
		self.msgNum = setNameToMsg[setName]
		
	def addKana(self, kana):
		self.kana.add(kana)

	def addPortion(self, portion):
		self.portions.append(portion)

	# add all active kana to the given list
	def getActiveKana(self, answerSet = None):
		if answerSet is None:
			answerSet = set()
                        
		if not self.active:
			return answerSet

		for portion in self.portions:
			portion.getActiveKana(answerSet)

		return answerSet

portionIndex = 28
class KanaPortion(object):
	"""The finest collection grade for kana, kana of similar types."""
	def __init__(self, kind, set):
		self.members = []
		self.active = 0
		global portionIndex
		self.msgNum = portionIndex
		portionIndex += 1
		self.kind = kind
		self.set = set

		self.optionKey = set.optionKey + "_portions"

	def addKana(self, kana):
		self.members.append(kana)

	def __contains__(self, object):
		return object in self.members

	def __str__(self):
		return (" ".join([str(x) for x in self.members])).upper()

	def getActiveKana(self, answerSet = None):
		if answerSet is None:
			answerSet = set()
			
		if not self.active:
			return answerSet

		for member in self.members:
			answerSet.add(member)

		return answerSet

class Kana(object):
	"""Represents a single Kana, and knows all romanizations of it."""
	def __init__(self, kana, kanaKind, kanaSet, kanaPortion):
		self.kana = kana
		self.transcriptions = {}
		self.kind = kanaKind
		self.set = kanaSet
		self.portion = kanaPortion
		
		for transcription in transcriptions:
			self.transcriptions[transcription] = \
		        HepburnToOtherSysConvert(kana, transcription)

	# Theoretically, we probably "ought" to stringify these as their
	# Unicode representations. Realistically, the romaji are probably
	# easier to deal with for us gaijin.
	def __str__(self):
		return self.kana
	def __repr__(self):
		return "<Kana: %s in %s>" % (self.kana, self.kind.kind)
	def __hash__(self):
		return hash(self.kana)
	def __eq__(self, other):
		return self.kana == other.kana

# Now, from the data here, construct the Kana data structures
i = 0
for kanaKindName in order:
	setName, kindName = kanaKindName.split(' ')
	kanaKind = kanaKinds[kindName]
	kanaSet = kanaKind.getSet(setName)
	kanaSets.append(kanaSet)
	kanaSetByName[setName + " " + kindName[0].upper() + kindName[1:]] = kanaSet
	i += 1
	setMembers = kanaList[kanaKindName]

	for kanaPortion in setMembers:
		portion = KanaPortion(kanaKind, kanaSet)
		kanaSet.addPortion(portion)
		for kana in kanaPortion:
			kana = Kana(kana, kanaKind, kanaSet, portion)
			portion.addKana(kana)
			kanaSet.addKana(kana)
			kanaKind[kana.kana] = kana
