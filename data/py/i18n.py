# -*- coding: utf-8 -*-
"""Kana no quiz!

   Copyleft 2003, 2004, 2005, 2006, 2007, 2008, 2009 Choplair-network.
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
   def __init__(self, path):
      self.currlang = str()
      self.localepath = path

   def setlang(self, lang):
      if lang == "en":
         global _
         def _(msg): return msg
      else: 
         try:   #Removing the global _ if the current language is english.
            if self.currlang == "en": del _
         except: pass

         gettext.translation("kana-no-quiz", self.localepath, [lang]).install()

      self.currlang = lang #Update the current language variable.

   def msg(self,num):
      # Tuple of commom strings.
      strings = (
         _("Kana no quiz!"),  # 0
         _("Introduction"),
         _("Options"),
         _("Start the quiz"),
         _("About"),
         _("Two different writing systems are commonly used by the Japanese: "
            "kanji & kana."),  # 5
         _("Kanji are complex ideograms retranscribing words whereas kana "
            "are simple symbols used as syllables which have to be "
            "combined to make words. Any word in Japanese can be written "
            "using kana, it is like an alphabet."),
         _("There are two kinds of kana: hiragana & katakana. Hiragana is "
            "the most-used traditional syllabary used to write Japanese "
            "words. Katakana is a larger syllabary, with more sounds, "
            "mostly used to write proper nouns and loanwords of foreign "
            "origin."),
         _("Kana no quiz helps you to memorize kana and their associated "
            "sound, using transcription systems. For more simplicity, "
            "syllables have been split in multiple sets, and you can even "
            "choose to learn only a portion of kana at a time."),
         _("Have a good practice ! ^_^"),
         _("OK"),  # 10
         _("What is this katakana?"),
         _("What is this hiragana?"),
         _("Right! ^^"),
         _("Wrong!"),
         _("The answer was %s."),  # 15
         _("Quiz results"),
         _("Question total: %i."),
         _("Good answers: %i."),
         _("Success rate: %i%%."),
         _("Here you can modify some quiz options."),  # 20
         _("Hiragana question sets"),
         _("Katakana question sets"),
         _("Basic"),
         _("Modified"),
         _("Contracted"),  # 25
         _("Additional"),
         _("Portions"),
         _("Hiragana"),
         _("Katakana"),
         _("Basic set"),  # 30
         _("Modified set"),
         _("Contracted set"),
         _("Additional set"),
         _("Additional katakana"),
         _("If you are novice, it may be interesting at the beginning to "
            "train yourself only on portions instead of the full kana set."),  # 35
         _("Select the kana portions you want to train yourself upon:"),
         _("Select all"),
         _("Answering method:"),
         _("A random list"),
         _("A text entry"),  # 40
         _("Random answer list size:"),
         _("%s choices"),
         _("Quiz length:"),
         _("Don't repeat the same kana\n(as much as possible)."),
         _("Language:"),  # 45
         _("English"),
         _("French"),
         _("Portuguese (Brazil)"),
         _("Serbian"),
         _("Swedish"),  # 50
         _("Save"),
         _("Cancel"),
         _("A Japanese kana memorization tool."),
         _("Version %s."),
         _("Kana no quiz is free software with its source code released under "
         "the terms of the GNU General Public License (see `GPL.txt').\nThe "
         "whole multimedia content is released under the terms of the Free "
         "Art license (see `FAL.txt') with the exception of the kana image "
            "theme that was adapted from \"Kana Test\", released under the "
            "GNU GPL as well."),  # 55
         _("Credits"),
         _("Main development: Choplair.\n"
            "Code contribution: Jeremy Bowers."),
         _("Close"),
         _("Warning"),
         _("Please select at least one kana portion to start the quiz."),  # 60
         _("Transcription system:"),
         _("Hepburn (most used)"),
         _("Kunrei-shiki"),
         _("Nihon-shiki"),
         _("Information"),  # 65
         _("Programming"),
         _("Question {0} of {1}."),
         _("%s system."),
         _("Stop"),
         _("German"),  # 70
         _("Quit"),
         _("Unrecognized katakana: %s."),
         _("Unrecognized hiragana: %s."),
         _("Russian"),
         _("Random answer selection range:"),  # 75
         _("Same kana portions"),
         _("Same kana set"),
         _("Same kana kind"),
         _("Polivanov (cyrillic)"),
         _(" questions."),  # 80
         _("Translations"),
         _("Brazilian: Matheus Villela.\n"
            "French: Choplair.\n"
            "Galician: Rafael López García.\n"
            "German: Florian Niemann.\n"
            "Russian: Aleksej R. Serdyukov.\n"
            "Serbian: Dejan Danilovic.\n"
            "Spanish: Rafael López García.\n"
            "Swedish: Markus Fellnert."),
         _("Kana"),
         _("Answering"),
         _("Sound"),  #85
         _("Misc."),
         _("Kana tables"),
         _("Welcome to Kana no quiz version %s."),
         _("Crappy!"),
         _("Average"),  # 90
         _("Good"),
         _("Excellent!"),
         _("Here comes the complete kana tables, sorted respecting the "
            "Japanese traditional order (except for additional katakana "
            "that haven't been standardized)."),
         _("You may enjoy full kana list overview (with transcription), "
            "select the portions you want to be trained upon, and see larger "
            "image when clicking on a thumbnail."),
         _("Kana image scale:"),  # 95
         _("Small"),
         _("Medium"),
         _("Large"),
         _("Kana image theme:"),
         _("Modern colorful"),  # 100
         _("Traditionnal black & white"),
         _("Kana vocal pronouncing"),
         _("Female: Myrtille Chouard.\n"
           "Male: Pachilor."),
         _("Kana image themes"),
         _("Modern colorful: Ms. Marie-Claire.\n"
           "Traditional black & white:\n"
           "adapted from \"Kana Test\"."),  # 105
         _("Artworks"),
         _("Fayanne & Choplair."),
         _("Kana vocal pronouncing:"),
         _("Female"),
         _("Male"),  # 110
         _("Both alternately"),
         _("Spanish"),
         _("Galician"),
         _("Please restart Kana no quiz for the language change to take "
            "effect."),
         )

      return strings[num]
