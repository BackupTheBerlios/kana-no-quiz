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
import random

class KanaEngine:
	def __init__(self):
		self.previous_kana = None
		#Kana lists.
		self.kana_sets = (
		[ #Basic.
		"a",	"i",	"u",	"e",	"o",
		"ka",	"ki",	"ku",	"ke",	"ko",
		"sa",	"shi",	"su",	"se",	"so",
		"ta",	"chi",	"tsu",	"te",	"to",
		"na",	"ni",	"nu",	"ne",	"no",
		"ha",	"hi",	"fu",	"he",	"ho",
		"ma",	"mi",	"mu",	"me",	"mo",
		"ya",		"yu",		"yo",
		"ra",	"ri",	"ru",	"re",	"ro",
		"wa",				"o-2",
		"n"],
		[ #Modified.
		"ga",	"gi",	"gu",	"ge",	"go",
		"za",	"ji",	"zu",	"ze",	"zo",
		"da",	"ji-2",	"zu-2",	"de",	"do",
		"ba",	"bi",	"bu",	"be",	"bo",
		"pa",	"pi",	"pu",	"pe",	"po"],
		[ #Contracted.
		"kya",		"kyu",		"kyo",
		"sha",		"shu",		"sho",
		"cha",		"chu",		"cho",
		"nya",		"nyu",		"nyo",
		"rya",		"ryu",		"ryo",
		"gya",		"gyu",		"gyo",
		"ja",		"ju",		"jo",
		"bya",		"byu",		"byo",
		"pya",		"pyu",		"pyo"],
		[ #Additional (katakana only).
					"ye",
			"wi",		"we",	"wo",
		"kwa",				"kwo",
		"gwa",
					"she",
					"je",
					"che",
		"tsa",			"tse",	"tso",
			"ti",	"tu",
			"di",	"du",
			"tyu",	"dyu",
		"fa",	"fi",		"fe",	"fo",
		"va",	"vi",	"vu",	"ve",	"vo"])

	def randomKana(self,*args):
		if "true" in args:
			#Selection of syllabary kind.
			if "true" in args[0:4] and "true" in args[4:7]: self.kind = random.choice((0,1))
			elif "true" in args[0:4]: self.kind = 0
			else: self.kind = 1

			#Selecton of possible question sets.
			possible_sets = []

			i = 0
			for x in (args[0:4],args[4:7])[self.kind]:
				if x=="true": possible_sets.append(self.kana_sets[i])
				i+=1

			#Selection of THE question set.
			if len(possible_sets)>1: self.question_set = random.choice(possible_sets)
			else: self.question_set = possible_sets[0]

			#Selection of the kana.
			#We prevent the previous kana of being selected again.	
			if self.previous_kana and (self.previous_kana[0],self.previous_kana[1])==(self.kind,self.question_set):
				self.question_set.remove(self.previous_kana[2]) #We remove the previous kana from the list.
				self.kana = random.choice(self.question_set) #Kana selection.
				self.question_set.append(self.previous_kana[2]) #We can now safety re-append it to the list.
			else: self.kana = random.choice(self.question_set) #Kana selection.

			self.previous_kana = (self.kind,self.question_set,self.kana) #Precisely memorize this kana to prevent it to be selected the next time.

			return self.kana

		else: return 0

	def getKanaKind(self):
		#Katakana = 0 & hiragana = 1.
		if self.kind==0: return 0
		else: return 1

	def randomAnswers(self,list_size):
		templist = list(self.question_set) #Anwsers will be get from this temporary question set.
		answers = [] #Anwsers' list.

		for x in range(int(list_size)):
			if x==0: x = self.kana #Put the right anwser in the list.
			else: x = random.choice(templist) #Put random wrong anwsers from the kana list.

			#Prevent selection of kana with the same romanji transcription.
			if x[-2:]=="-2" and x[:-2] in templist: templist.remove(x[:-2])
			elif "%s-2" % x in templist: templist.remove("%s-2" % x)

			answers.append(x)
			templist.remove(x) #We remove it from the kana list to prevent multiple selection of the same kana...

		random.shuffle(answers)

		return answers
