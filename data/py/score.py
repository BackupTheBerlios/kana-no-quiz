"""
Kana no quiz!
Copyleft 2003 Choplair-network.

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
		self.total = 0 #Total question number.
		self.score = 0 #The score value.

	def update(self,point=0):
		self.total += 1 #Increment the total question number.
		self.score += point #Update the score.

	def isQuizFinished(self,length):
		if length=="short": num = 10
		elif length=="normal": num = 20
		elif length=="long": num = 30

		if self.total>=num: return 1
		else: return None

	def getResults(self):
		#Compute the success rate (percent).
		if self.total: successrate = self.score * 100 / self.total
		else: successrate = 0

		return self.total, self.score, successrate

	def reset(self):
		#Reset values...
		self.total = 0
		self.score = 0
