"""Kana no quiz!
   Copyleft 2003, 2004, 2005, 2006, 2007 Choplair-network.
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
class Score:
	def __init__(self):
		self.total = 0  # Total question number.
		self.score = 0  # The score value.
		# Unrecognized kana dicts (katakana or hiragana, with repetition number).
		self.unrecKana = [{},{}]

	def update(self, point, kana=None, kind=0):
		self.total += 1  # Incrementing the total question number.
		self.score += point  # Updating the score.

		if point == 0: # If wrong answer, taking note of the unrecognized kana.
			# This kana has yet been unrecognized: incrementing value.
			if self.unrecKana[kind].has_key(kana):
				self.unrecKana[kind][kana] += 1
			else:  # Setting value 1 to this kana in the wrong answer list.
				self.unrecKana[kind][kana] = 1

	def is_quiz_finished(self,length):
		if self.total >= int(length): return True
		else: return False

	def get_question_total(self): return self.total

	def get_results(self):
		# Compute the success rate (percent).
		if self.total: successrate = self.score * 100 / self.total
		else: successrate = 0

		# Postformating unrecognized kana dicts.
		unrecKanaPF = [{},{}]
		for i in range(2):
			for key, val in self.unrecKana[i].items():
				if unrecKanaPF[i].has_key(val): unrecKanaPF[i][val].append(key)
				else: unrecKanaPF[i][val] = [key]
			unrecKanaPF[i].keys().sort()
			unrecKanaPF[i].keys().reverse()

		return self.total, self.score, successrate, unrecKanaPF

	def reset(self):
		# Reseting values...
		self.__init__()
