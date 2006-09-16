# -*- coding: utf8 -*-
"""Test the kana objects."""

import unittest
import sys
import os
if __name__ != "__main__":
	f = __file__
	f = os.path.normpath(os.path.dirname(f) + os.sep + os.pardir)
	if f not in sys.path: sys.path.append(f)
else:
	if os.pardir not in sys.path:
		sys.path.append(os.pardir)

import kanaengine
import options

class KanaTest(unittest.TestCase):
	"""Does the kana data structure work as expected?"""

	def testBasicData(self):
		"""basic kana data structure seems to work"""
		hiragana = kanaengine.hiragana
		shi = hiragana['shi']

		self.assertEquals(shi.kana, 'shi')
		self.assertEquals(shi.transcriptions['hepburn'], 'shi')
		self.assertEquals(shi.transcriptions['polivanov'], "си")

		shiPortion = shi.portion
		self.assertEquals(str(shiPortion), 'SA SHI SU SE SO')
		self.assert_(shi in shiPortion)

		# Kana can be stringified
		self.assertEquals(repr(shi), "<Kana: shi in hiragana>")
		self.assertEquals(str(shi), "shi")

# This ought to be standard in Python, to complement setattr
def setitem(obj, key, value):
	obj[key] = value

# This may later get pulled out into its own 'optionsTest.py' file.
class OptionsTest(unittest.TestCase):
	"""Does the options stuff work as expected?"""
	def testOptionSetting(self):
		"""options works as a python dict"""
		opts = options.Options()

		opts['answer_mode'] = 'list'
		self.assertEquals(opts['answer_mode'], 'list')
		self.assertRaises(ValueError, setitem, opts, 'answer_mode',
						  'fromage')

		# Now, try the basic_hiragana_portions to see if the active
		# flag is correctly set
		basicHiragana = kanaengine.kanaSetByName['Basic Hiragana']
		portions = basicHiragana.portions

		# Verify that when setting the _portions options, it
		# gets transmitted to the .active flag on the portion
		portionSettings = (1,0,1,0,0,1,0,0,1)
		opts['basic_hiragana_portions'] = portionSettings
		for active, portion in zip (portionSettings, portions):
			self.assertEquals(portion.active, active)

        # Verify that when setting the names of sections, the active
        # flag is set correctly
		for optionName, kanaSet in kanaengine.kanaSetByOptionKey.iteritems():
			opts[optionName] = 'true'
			self.assert_(kanaSet.active)
			opts[optionName] = 'false'
			self.assert_(not kanaSet.active)

	def testLiveActiveFlags(self):
		"""KanaPortion.active flags are directly reflected in the options"""
		opts = options.Options()
		vowels = kanaengine.kanaSetByName['Basic Hiragana'].portions[0]

		self.assertEquals(opts['basic_hiragana_portions'][0] + 0,
						  vowels.active)
		vowels.active = True
		self.assertEquals(opts['basic_hiragana_portions'][0] + 0,
						  vowels.active)
		vowels.active = False
		self.assertEquals(opts['basic_hiragana_portions'][0] + 0,
						  vowels.active)
		opts['basic_hiragana_portions'] = (0,0,0,0,0,0,0,0,0)
		self.assertEquals(vowels.active, False)
		opts['basic_hiragana_portions'] = (1,0,0,0,0,0,0,0,0)
		self.assertEquals(vowels.active, True)

class AnswersTest(unittest.TestCase):
	"""Does the answers portion of the engine work as expected?"""

	def testRandomAnswers(self):
		"""random wrong answers engine seems to work correctly"""
		engine = kanaengine.KanaEngine(options.Options())

		hiragana = kanaengine.hiragana
		shi = hiragana['shi']
		
		opts = options.Options()
		# Reset the hiragana portions so we know the s's are
		# currently active
		opts['basic_hiragana_portions'] = (1,1,1,1,1,1,1,1,1)
		opts['basic_hiragana'] = 'true'

		shiPortion = shi.portion
		self.assertEquals(str(shiPortion), 'SA SHI SU SE SO')
		sa, shi, su, se, so = shiPortion.members

		opts['allow_repetition'] = 'false'
		opts['rand_answer_sel_range'] = 'portion'

		answers = engine.randomAnswers(4, shi)
		self.assertEquals(len(answers), 4)
		self.assert_(shi in answers)
		
		answers = engine.randomAnswers(2, shi)
		self.assertEquals(len(answers), 2)
		self.assert_(shi in answers)

	def testRandomKana(self):
		"""random answer engine seems to work correctly"""

		# There is a lot of repetition in this test,
		# but I currently do not yet have the tools to
		# cut it down
		opts = options.Options()        
		engine = kanaengine.KanaEngine(opts)

		hiragana = kanaengine.hiragana
		shi = hiragana['shi']

		# Nail down the active kana to just sa, shi, su, se, and so
		for kanaSet in kanaengine.kanaSetByName.values():
			kanaSet.active = False
			for portion in kanaSet.portions:
				portion.active = False

		# Now, turn on just Basic Hiragana and the s line
		opts = options.Options()

		for kanaSet in kanaengine.kanaSetByOptionKey.keys():
			opts[kanaSet] = 'false'
			
		opts['basic_hiragana'] = 'true'
		opts['basic_hiragana_portions'] = (0,0,1,0,0,0,0,0,0)

		sPortion = shi.portion
		basicHiragana = shi.set
		self.assert_(sPortion.active)
		self.assert_(basicHiragana.active)

		# The hiragana starting with "S"
		sKana = sPortion.members

		opts['allow_repetition'] = 'true'
		opts['rand_answer_sel_range'] = 'portion'

		answer = engine.randomKana()
		self.assert_(answer in sKana)

		# Verify that the previous kana never gets picked
		for i in range(100):
			nextAnswer = engine.randomKana()
			self.assertNotEquals(nextAnswer, answer)
			self.assert_(answer in sKana)
			answer = nextAnswer

		# Open up the entire Basic Hiragana set and repeat
		opts['basic_hiragana_portions'] = (1,1,1,1,1,1,1,1,1)
		opts['basic_hiragana'] = 'true'

		engine = kanaengine.KanaEngine(opts)
		opts['rand_answer_sel_range'] = 'set'
		basicHiraganaSet = basicHiragana.getActiveKana()
		answer = engine.randomKana()
		self.assert_(answer in basicHiraganaSet)
		
		# Verify we drew from more than one portion
		distinctKana = set()
		for i in range(100):
			nextAnswer = engine.randomKana()
			distinctKana.add(nextAnswer)
			self.assertNotEquals(nextAnswer, answer)
			self.assert_(answer in basicHiraganaSet)
			answer = nextAnswer
			
		# Probability of this being false if the code is
		# working correctly are about 0
		self.assert_(len(distinctKana) > 20)

		# Open up the entire Hiragana kind and repeat,
		# really need to get this slicker
		opts['modified_hiragana_portions'] = (1,1,1,1,1)
		opts['modified_hiragana'] = 'true'
		opts['contracted_hiragana_portions'] = (1,1,1,1,1)
		opts['contracted_hiragana'] = 'true'
		
		engine = kanaengine.KanaEngine(opts)
		opts['allow_repetition'] = 'true'
		opts['rand_answer_sel_range'] = 'set'

		hiraganaKana = hiragana.getActiveKana()
		
		answer = engine.randomKana()
		self.assert_(answer in hiraganaKana)
		
		distinctKana = set()
		for i in range(100):
			nextAnswer = engine.randomKana()
			distinctKana.add(nextAnswer)
			self.assertNotEquals(nextAnswer, answer)
			self.assert_(answer in hiraganaKana)
			answer = nextAnswer

		self.assert_(len(distinctKana) > 50)

if __name__ == "__main__":
	unittest.main()

