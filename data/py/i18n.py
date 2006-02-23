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
import gettext

class I18n:
	def __init__(self,path):
		self.currlang = str()
		self.localepath = path

	def setlang(self,lang):
		if lang=="en":
			global _
			def _(msg): return msg
		else: 
			try:	#Remove the global _ if the current language is english.
				if self.currlang=="en": del _
			except: pass

			gettext.translation("kana-no-quiz",self.localepath,[lang]).install()

		self.currlang = lang #Update the current language variable.

	def str(self,num):
		# Tuple of commom strings.
		string = (
			_("Kana no quiz!"), #0
			_("Introduction"),
			_("Options"),
			_("Start the quiz"),
			_("About"),
			_("Two different writing systems are commonly used by Japaneses: kanji & kana."), #5
			_("Kanji are complex ideograms retranscribing words whereas kana are simple symbols used as syllables which have to be combined to make words. Any word in Japanese can be written using kana, it is like an alphabet."),
			_("There are two kinds of kana: hiragana & katakana. Hiragana is the most-used traditional syllabary used to write Japanese words. Katakana is a larger syllabary, with more sounds, mostly used to write proper nouns and loanwords of foreign origin."),
			_("Kana no quiz helps you to memorize kana and their associated sound (using the Hepburn's roman transcription system). For more simplicity, syllables have been split in multiple sets, and you can even choose to learn only a portion of kana at a time."),
			_("Have a good practice ! ^_^"),
			_("OK"), #10
			_("What is this katakana?"),
			_("What is this hiragana?"),
			_("Right! ^^"),
			_("Wrong!"),
			_("The answer was %s."), #15
			_("Quiz results"),
			_("Question total: %i."),
			_("Good answers: %i."),
			_("Success rate: %i%%."),
			_("Here you can modify some quiz options."), #20
			_("Hiragana question sets"),
			_("Katakana question sets"),
			_("Basic"),
			_("Modified"),
			_("Contracted"), #25
			_("Additional"),
			_("Parts"),
			_("Basic hiragana parts"),
			_("Modified hiragana parts"),
			_("Contracted hiragana parts"), #30
			_("Basic katakana parts"),
			_("Modified katakana parts"),
			_("Contracted katakana parts"),
			_("Additional katakana parts"),
			_("If you are novice, it may be interesting at the beginning to train yourself only on some kana instead of the full set."), #35
			_("Select the kana portions you want to train yourself upon:"),
			_("Select all"),
			_("Answer mode:"),
			_("A random list"),
			_("A text entry"), #40
			_("Random answer list size:"),
			_("%s choices"),
			_("Length:"),
			_("Don't repeat the same kana\n(as much as possible)."),
			_("Language:"), #45
			_("English"),
			_("French"),
			_("Portuguese (Brazil)"),
			_("Serbian"),
			_("Swedish"), #50
			_("Save"),
			_("Cancel"),
			_("Kana no quiz, a kana reminder tool."),
			_("Version %s."),
			_("Kana no quiz is free software released under the GNU GPL license (see `GPL.txt'). Kana images are released under the Free Art license (see `FAL.txt')."), #55
			_("Credits"),
			_("Coding: Choplair & Pachilor.\nKana image: Ms. Marie-Claire.\nLogo image: Choplair."),
			_("Close"),
			_("Warning"),
			_("You must select at least one question set."), #60
			_("Romanization system:"),
			_("Hepburn (recommended)"),
			_("Kunrei-shiki"),
			_("Nihon-shiki"),
			_("Information"), #65
			_("No portion selected: that question set is disabled. :p"),
			_("Question %s of %s."),
			_("%s system."),
			_("Stop"),
			_("German"), #70
			_("Quit")
			)

		return string[num]
