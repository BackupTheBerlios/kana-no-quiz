"""
Kana no quiz!
Copyleft 2003, 2004 Choplair-network.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either self.version 2
of the License, or (at your option) any later self.version.

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
	def __init__(self):
		self.currlang = str()

	def setlang(self,lang):
		if lang=="en":
			global _
			def _(msg): return msg
		else: 
			try:	#Remove the global _ if the current language is english.
				if self.currlang=="en": del _
			except: pass

			gettext.translation("kana-no-quiz","data/locale/",[lang]).install()

		self.currlang = lang #Update the current language variable.

	def str(self,num):
		# Tuple of commom strings.
		string = (
			_("Kana no quiz!"), #0
			_("Start"),
			_("Options"),
			_("About"),
			_("What is this katakana?"),
			_("What is this hiragana?"), #5
			_("Right! ^^"),
			_("Wrong!"),
			_("The answer was %s."),
			_("Quiz results"),
			_("Question total: %i."), #10
			_("Good answers: %i."),
			_("Success rate: %i%%."),
			_("Here you can modify some quiz options."),
			_("Katakana question sets"),
			_("Hiragana question sets"), #15
			_("Basic"),
			_("Modified"),
			_("Contracted"),
			_("Additional"),
			_("Answer mode:"), #20
			_("A random list"),
			_("A text entry"),
			_("Random answer list size:"),
			_("2 choices"),
			_("3 choices"), #25
			_("4 choices"),
			_("Length:"), 
			_("Short (10 questions)"),
			_("Normal (20 questions)"),
			_("Long (30 questions)"), #30
			_("Language:"),
			_("English"),
			_("French"),
			_("Spanish"),
			_("Swedish"), #35
			_("Save"),
			_("Cancel"), 
			_("Kana no quiz, a kana reminder tool."),
			_("Version %s."),
			_("Kana no quiz is free software released under the GNU GPL license (see `GPL.txt'). Kana images are released under the Free Art license (see `FAL.txt')."), #40
			_("Credits"),
			_("Code: Choplair & Pachilor.\nKana image: Ms. Marie-Claire.\nLogo image: Choplair."),
			_("Close"),
			_("Warning"),
			_("You must select at least one question set.") #45
			)

		return string[num]
