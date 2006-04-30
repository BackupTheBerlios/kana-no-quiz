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
# This is the Tkinter interface, mainly designed for Windows user.

import Tkinter as tk
import tkMessageBox
import os.path
import kanaengine, score, i18n
from string import capwords

class Gui:
	def __init__(self,*args):
		self.param = args[0]
		self.version = args[1]
		self.datarootpath = args[2]

		self.window = tk.Tk()
		self.kanaEngine = kanaengine.KanaEngine()
		self.score = score.Score()
		self.dialogState = {"about":0,"kanaPortionPopup":0}
		self.main_win_geom = None

		#Localization.
		self.i18n = i18n.I18n(os.path.join(self.datarootpath,"locale"))
		self.currentlang = self.param.val('lang')
		self.i18n.setlang(self.param.val('lang'))
		global str
		str = self.i18n.str

		#Initial window attributes.
		self.window.resizable(0,0)

	def main(self,event=None):
		if self.currentlang!=self.param.val('lang'):
			#Changing localization...
			self.currentlang = self.param.val('lang')
			self.i18n.setlang(self.param.val('lang'))
			global str
			str = self.i18n.str

		self.window.title(str(0))
		frame = tk.Frame(self.window)
		frame.pack(padx=2,pady=2)

		#Logo.
		img = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","logo.gif"))
		label = tk.Label(frame,image=img)
		label.pack(side="left")

		frame2 = tk.Frame(frame)
		frame2.pack(fill="both",expand=1)
		button = tk.Button(frame2,text=str(1),command=self.intro)
		button.pack(fill="both",expand=1)
		button = tk.Button(frame2,text=str(2),command=self.options)
		button.pack(fill="both",expand=1)
		button = tk.Button(frame2,text=str(3),command=self.quiz)
		button.pack(fill="both",expand=1)
		button = tk.Button(frame2,text=str(4),command=self.about)
		button.pack(fill="both",expand=1)
		button = tk.Button(frame2,text=str(71),command=self.quit)
		button.pack(fill="both",expand=1)

		self.window.mainloop()
		
	def intro(self):
		def goBack():
			self.window.slaves()[0].destroy()
			self.main()

		self.window.slaves()[0].destroy()
		self.window.title(str(1)) #Changeing window title.

		frame = tk.Frame(self.window)
		frame.pack(padx=2,pady=2)

		label = tk.Label(frame,text=str(5),wraplength=420)
		label.pack(side="top")
		label = tk.Label(frame,text=str(6),wraplength=420)
		label.pack(side="top")
		label = tk.Label(frame,text=str(7),wraplength=420)
		label.pack(side="top")
		label = tk.Label(frame,text=str(8),wraplength=420)
		label.pack(side="top")
		label = tk.Label(frame,text=str(9),wraplength=420)
		label.pack(side="top")
		button = tk.Button(frame,text=str(10),command=goBack)
		button.pack(side="top",fill="both",expand=1)

	def quiz(self):
		#Defining kana selection parameters.
		self.kanaEngine.kanaSelectParams(
			(self.param.val('basic_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('contracted_hiragana'),
			self.param.val('basic_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('contracted_katakana'),
			self.param.val('additional_katakana')),
			(self.param.val('basic_hiragana_portions'),
			self.param.val('modified_hiragana_portions'),
			self.param.val('contracted_hiragana_portions'),
			self.param.val('basic_katakana_portions'),
			self.param.val('modified_katakana_portions'),
			self.param.val('contracted_katakana_portions'),
			self.param.val('additional_katakana_portions')),
			self.param.val('kana_no_repeat'),
			self.param.val('rand_answer_sel_range'))
		#Randomly getting a kana (respecting bellow conditions).
		self.kana = self.kanaEngine.randomKana()

		if self.kana:
			self.quizWidget = {}
			self.window.slaves()[0].destroy()
			frame = tk.Frame(self.window)
			frame.pack(padx=3,pady=3)
			self.quizWidget["left_part"] = tk.Frame(frame)

			#Kana image.
			self.image = tk.PhotoImage()
			self.setKanaImage(self.kanaEngine.getKanaKind(),self.kana)  #Initialy setting kana's image.
			self.quizWidget["kanaImage"] = tk.Label(self.quizWidget["left_part"],image=self.image,border=0)
			self.quizWidget["kanaImage"].pack(side="top")

			#Quiz informations.
			frame3 = tk.Frame(self.quizWidget["left_part"])
			self.quizWidget['questionNumLabel'] = tk.Label(frame3,bd=0,text=str(67) % (self.score.getQuestionTotal()+1,self.param.val('length')),bg="white")
			self.quizWidget['questionNumLabel'].pack(expand=1,fill="both")
			self.quizWidget['systemLabel'] = tk.Label(frame3,bd=0,text=str(68) % capwords(self.param.val('transcription_system')),bg="white")
			self.quizWidget['systemLabel'].pack(expand=1,fill="both")
			frame3.pack(side="top",expand=1,fill="both")
			self.quizWidget["left_part"].pack(side="left",expand=1,fill="both")

			self.quizWidget["right_part"] = tk.Frame(frame)
			self.quizWidget["right_part"].pack(padx=6,side="right",fill="both",expand=1)

			#Stop button.
			self.quizWidget['stopframe'] = tk.Frame(self.quizWidget["right_part"])
			self.quizWidget['stopframe'].pack(fill="x",side="top")
			self.quizWidget['stop'] = tk.Button(self.quizWidget['stopframe'],text=str(69),command=self.results)
			#Question label.
			self.quizWidget['quiz_label']= tk.Label(self.quizWidget["right_part"],text=(str(11),str(12))[self.kanaEngine.getKanaKind()],wraplength=150,width=24)
			self.quizWidget['quiz_label'].pack(pady=3,fill="both",expand=1)

			#The arrow.
			self.nextButton = tk.Button(self.quizWidget["right_part"],bitmap="@%s" % os.path.join(self.datarootpath,"img","rarrow.xbm"),pady=4)

			if self.param.val('answer_mode')=="list":
				#Choice buttons generation.
				self.answerButt = {}; i=0
				for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
					#If the selected romanization system is *other* than Hepburn (default),
					#let's convert that answer list (given in the Hepburn internal format)
					#into the user-selected romanization system.
					if self.param.val('transcription_system')!="hepburn":
						x = kanaengine.HepburnToOtherSysConvert(x,self.param.val('transcription_system'))

					if x[-2:]=="-2": x = x[:-2]
					self.answerButt[i] = tk.Button(self.quizWidget["right_part"],text=x.upper(),height=2)
					self.answerButt[i].bind("<ButtonRelease-1>",self.checkAnswer)
					self.answerButt[i].pack(pady=1,fill="both",expand=1)
					i+=1

				self.nextButton['command'] = self.newQuestion
			else:
				self.answerButt = tk.Entry(self.quizWidget["right_part"],width=17)
				self.answerButt.pack()
				self.nextButton['command'] = self.checkAnswer
				self.nextButton.pack(fill="both",pady=1,expand=1)

		else:	tkMessageBox.showwarning(str(59),str(60))

	def checkAnswer(self,event=None):
		"""Checking the given answer, updating the score
		and displaying the result."""
		if self.param.val('answer_mode')=="list": answer = event.widget["text"].lower().encode('utf8')
		else: answer = self.answerButt.get().lower().encode('utf8')

		#If the selected romanization system is *other* than Hepburn (default),
		#let's convert the good answer (given in the Hepburn internal format)
		#to the user-selected romanization system, in order to compare with its
		#chosen answer.
		if self.param.val('transcription_system')!="hepburn":
			self.kana = kanaengine.HepburnToOtherSysConvert(self.kana,self.param.val('transcription_system'))
		if self.kana[-2:]=="-2": self.kana = self.kana[:-2]

		if answer==self.kana: # \o/
			self.quizWidget['quiz_label']["text"] = str(13)
			self.quizWidget['quiz_label']["fg"] = "darkgreen"
			self.score.update(1) #Updating the score (adding 1 point).

		else: # /o\
			self.quizWidget['quiz_label']["text"] = "%s\n%s" % (str(14), str(15) % self.kana.upper())
			self.quizWidget['quiz_label']["fg"] = "red"
			self.score.update(0,self.kana,self.kanaEngine.getKanaKind()) #Updating the score (indicating unrecognized kana).

		if self.param.val('answer_mode')=="list":
			for butt in self.answerButt.values(): butt.pack_forget() #Hide choices buttons.
			self.nextButton.pack(fill="both",pady=1,expand=1)
		else:
			self.answerButt.pack_forget()
			self.nextButton['command'] = self.newQuestion

		if self.score.isQuizFinished(self.param.val('length')):
			#The quiz is finished... Let's show results!
			self.nextButton["command"]  = self.results
		else: self.quizWidget['stop'].pack(fill="both",expand=1)

	def newQuestion(self):
		self.kana = self.kanaEngine.randomKana() #Randomly get a kana.
		self.setKanaImage(self.kanaEngine.getKanaKind(),self.kana) #Update kana's image.

		self.quizWidget['questionNumLabel']["text"] = str(67) % (self.score.getQuestionTotal()+1,self.param.val('length'))
		self.quizWidget['quiz_label']["text"] = (str(11),str(12))[self.kanaEngine.getKanaKind()]
		self.quizWidget['quiz_label']["fg"] = "black"

		if self.param.val('answer_mode')=="list":
			self.nextButton.pack_forget() #Hide the arrow.
			#Display the random list.
			i=0
			for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
				#If the selected romanization system is *other* than Hepburn (default),
				#let's convert that answer list (given in the Hepburn internal format)
				#into the user-selected romanization system.
				if self.param.val('transcription_system')!="hepburn":
					x = kanaengine.HepburnToOtherSysConvert(x,self.param.val('transcription_system'))
				if x[-2:]=="-2": x = x[:-2]
				self.answerButt[i]["text"] = x.upper()
				self.answerButt[i].pack(pady=1,fill="both",expand=1)
				i+=1

		else: #Display the text entry.
			self.answerButt.delete(0,tk.END)
			self.nextButton.pack_forget()
			self.answerButt.pack()
			self.nextButton.pack(fill="both",pady=1,expand=1)
			self.nextButton['command'] = self.checkAnswer
	
		self.quizWidget['stop'].pack_forget() #Hiding the stop button.
		self.quizWidget['stopframe']['height'] = 1 #Reducing its container.

	def results(self):
		def goBack():
			self.window.slaves()[0].pack_forget()
			self.main()
		results = self.score.getResults()

		self.quizWidget["left_part"].pack_forget() #Removing left part (kana image...).

		#Displaying results.
		text = "\n%s\n\n%s\n%s\n%s" % (str(16),str(17) % results[0],str(18) % results[1],str(19) % results[2])

		def getUnrecStr(kind):
			"""Returning a ready-to-display string which indicates the
			unrecognized kana (by kind) during the quiz."""
			plop = ""
			for key,val in results[3][kind].items():
				for x in val: 
					if key!=1: plop += "%s (%s), " % (x.upper(),key)
					else: plop += "%s, " % x.upper()
			return "\n%s" % str(72+kind) % plop[:-2]

		if len(results[3][0])>0: text += getUnrecStr(0)
		if len(results[3][1])>0: text += getUnrecStr(1)
		
		self.quizWidget['quiz_label']["text"] = "%s\n" % text
		self.quizWidget['quiz_label']["fg"] = "black"
		self.quizWidget['quiz_label']['wraplength'] = 281
		self.quizWidget['quiz_label']['width'] = 42

		self.nextButton["command"] = goBack

		self.score.reset() #Reseting the score.
		self.quizWidget['stop'].pack_forget() #Hiding the stop button.
		self.quizWidget['stopframe']['height'] = 1 #Reducing its container.

	def options(self):
		#Dicts for integrer to string param convertion and vice-versa...
		opt_conv = {
			"boolean":{0:'false',1:'true','false':0,'true':1},
			"transcription_system":{str(62):"hepburn",str(63):"kunrei-shiki",str(64):"nihon-shiki",str(79):'polivanov','hepburn':str(62),'kunrei-shiki':str(63),'nihon-shiki':str(64),'polivanov':str(79)},
			"answer_mode":{str(39):'list',str(40):'entry','list':str(39),'entry':str(40)},
			"list_size":{str(42) % 2:2,str(42) % 3:3,str(42) % 4:4,str(42) % 5:5,2:str(42) % 2,3:str(42) % 3,4:str(42) % 4,5:str(42) % 5},
			"rand_answer_sel_range":{str(76):'portion',str(77):'set',str(78):'kind','portion':str(76),'set':str(77),'kind':str(78)},
			"lang":{str(46):'en',str(47):'fr',str(70):'de',str(48):'pt_BR',str(74):'ru',str(49):'sr',str(50):'sv','en':str(46),'fr':str(47),'de':str(70),'pt_BR':str(48),'ru':str(74),'sr':str(49),'sv':str(50)}
			}

		#Values for kana portion params.
		kanaPortions = [
			self.param.val('basic_hiragana_portions'),
			self.param.val('modified_hiragana_portions'),
			self.param.val('contracted_hiragana_portions'),
			self.param.val('basic_katakana_portions'),
			self.param.val('modified_katakana_portions'),
			self.param.val('contracted_katakana_portions'),
			self.param.val('additional_katakana_portions')]

		def goBack():
			self.window.slaves()[0].destroy()
			self.main()

		def save():
			self.param.write({
			'basic_hiragana':opt_conv["boolean"][option1.get()],
			'basic_hiragana_portions':kanaPortions[0],
			'modified_hiragana':opt_conv["boolean"][option2.get()],
			'modified_hiragana_portions':kanaPortions[1],
			'contracted_hiragana':opt_conv["boolean"][option3.get()],
			'contracted_hiragana_portions':kanaPortions[2],
			'basic_katakana':opt_conv["boolean"][option4.get()],
			'basic_katakana_portions':kanaPortions[3],
			'modified_katakana':opt_conv["boolean"][option5.get()],
			'modified_katakana_portions':kanaPortions[4],
			'contracted_katakana':opt_conv["boolean"][option6.get()],
			'contracted_katakana_portions':kanaPortions[5],
			'additional_katakana':opt_conv["boolean"][option7.get()],
			'additional_katakana_portions':kanaPortions[6],
			'transcription_system':opt_conv["transcription_system"][option8.get().encode('utf8')],
			'answer_mode':opt_conv["answer_mode"][option9.get().encode('utf8')],
			'list_size':opt_conv["list_size"][option10.get().encode('utf8')],
			'rand_answer_sel_range':opt_conv["rand_answer_sel_range"][option11.get().encode('utf8')],
			'length':int(option12.get()),
			'kana_no_repeat':opt_conv["boolean"][option13.get()],
			'lang':opt_conv["lang"][option14.get().encode('utf8')]
			})
			goBack() #Then, go back!

		def portions_popup(kanaset):
			temp_list = list(kanaPortions[kanaset]) #Temporary portion list.

			#Callbacks.
			class newValue:
				def __init__(self,num,var): self.num = num; self.var = var
				def plop(self):
					temp_list[self.num] = self.var.get() #Update the emporary variable value.
			class selectAll:
				def __init__(self,list): self.list = list
				def plop(self):
					"""Activate the check buttons."""
					i = 0
					for x in self.list:
						x.set(1)
						newValue(i,x).plop()
						i+=1
			def close():
				self.dialogState["kanaPortionPopup"] = 0
				dialog.destroy()

			def validedChanges():
				"""Check for a least one selected kana portion (display of a message
				if not the case), catch parameters, then close the window."""
				if not 1 in temp_list:
					tkMessageBox.showinfo(str(65),str(66))

					if kanaset==0: widget = option1
					elif kanaset==1: widget = option2
					elif kanaset==2: widget = option3
					elif kanaset==3: widget = option4
					elif kanaset==4: widget = option5
					elif kanaset==5: widget = option6
					elif kanaset==6: widget = option7
					widget.set(0)

				kanaPortions[kanaset] = temp_list
				close()

			#Check whether this dialog window is not opened yet.
			if not self.dialogState["kanaPortionPopup"]:
				self.dialogState["kanaPortionPopup"] = 1

				dialog = tk.Toplevel()
				dialog.resizable(0,0)
				dialog.title(str(28+kanaset))
				dialog.protocol("WM_DELETE_WINDOW",close)

				label = tk.Label(dialog,text=str(35),wraplength=350)
				label.pack()

				set = self.kanaEngine.getASet(kanaset)
				label = tk.Label(dialog,text=str(36),wraplength=350)
				label.pack()
				table = tk.Frame(dialog)
				table.pack()

				j,k = 1,0
				vars = []
				for i in range(len(set)):
					string = ""
					for kana in set[i]: string += "%s " % kana.upper()
					vars.append(tk.IntVar())
					c = tk.Checkbutton(table,text=string[:-1],variable=vars[i],command=newValue(i,vars[i]).plop)
					if temp_list[i]==1: c.select()
					if j: c.grid(column=0,row=k); j=0
					else: c.grid(column=1,row=k); j=1; k+=1

				button =  tk.Button(dialog,text=str(37),command=selectAll(vars).plop)
				#If nothing selected, select all. :p
				if not 1 in kanaPortions[kanaset]: button.invoke()
				button.pack()

				#Buttons at bottom..
				button = tk.Button(dialog,text=str(52),command=close)
				button.pack(side="right")
				button = tk.Button(dialog,text=str(51),command=validedChanges)
				button.pack(side="right")

		self.window.slaves()[0].destroy()
		self.window.title(str(2)) #Change title of window.

		frame = tk.Frame(self.window)
		frame.pack(padx=2,pady=2)
		label = tk.Label(frame,text=str(20))
		label.pack()

		option_frame = tk.Frame(frame)
		option_frame.pack(fill="both",expand=1)

		left_frame = tk.Frame(option_frame)
		left_frame.pack(fill="both",expand=1,side="left",pady=4)

		frame2 = tk.Frame(left_frame,relief="ridge",borderwidth=1)
		frame2.pack(fill="both",expand=1,pady=4)

		label = tk.Label(frame2,text=str(21))
		label.pack(fill="both",expand=1)
		table = tk.Frame(frame2)
		table.pack(fill="both",expand=1,padx=4)

		#`basic_hiragana'
		img5 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","basic_hiragana.gif"))
		label = tk.Label(table,image=img5)
		label.grid(column=0,row=0)
		option1 = tk.IntVar()
		option1.set(opt_conv["boolean"][self.param.val('basic_hiragana')])
		c = tk.Checkbutton(table,text=str(23),variable=option1)
		c.grid(column=1,row=0,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(0))
		button.grid(column=2,row=0)

		#`modified_hiragana'
		img6 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","modified_hiragana.gif"))
		label = tk.Label(table,image=img6)
		label.grid(column=0,row=1)
		option2 = tk.IntVar()
		option2.set(opt_conv["boolean"][self.param.val('modified_hiragana')])
		c = tk.Checkbutton(table,text=str(24),variable=option2)
		c.grid(column=1,row=1,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(1))
		button.grid(column=2,row=1)

		#`contracted_hiragana'
		img7 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","contracted_hiragana.gif"))
		label = tk.Label(table,image=img7)
		label.grid(column=0,row=2)
		option3 = tk.IntVar()
		option3.set(opt_conv["boolean"][self.param.val('contracted_hiragana')])
		c = tk.Checkbutton(table,text=str(25),variable=option3)
		c.grid(column=1,row=2,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(2))
		button.grid(column=2,row=2)

		frame2 = tk.Frame(left_frame,relief="ridge",borderwidth=1)
		frame2.pack(fill="both",expand=1,pady=6)

		label = tk.Label(frame2,text=str(22))
		label.pack(fill="both",expand=1)
		table = tk.Frame(frame2)
		table.pack(fill="both",expand=1,padx=4)

		#`basic_katakana'
		img1 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","basic_katakana.gif"))
		label = tk.Label(table,image=img1)
		label.grid(column=0,row=0)
		option4 = tk.IntVar()
		option4.set(opt_conv["boolean"][self.param.val('basic_katakana')])
		c = tk.Checkbutton(table,text=str(23),variable=option4)
		c.grid(column=1,row=0,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(3))
		button.grid(column=2,row=0)

		#`modified_katakana'
		img2 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","modified_katakana.gif"))
		label = tk.Label(table,image=img2)
		label.grid(column=0,row=1)
		option5 = tk.IntVar()
		option5.set(opt_conv["boolean"][self.param.val('modified_katakana')])
		c = tk.Checkbutton(table,text=str(24),variable=option5)
		c.grid(column=1,row=1,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(4))
		button.grid(column=2,row=1)

		#`contracted_katakana'
		img3 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","contracted_katakana.gif"))
		label = tk.Label(table,image=img3)
		label.grid(column=0,row=2)
		option6 = tk.IntVar()
		option6.set(opt_conv["boolean"][self.param.val('contracted_katakana')])
		c = tk.Checkbutton(table,text=str(25),variable=option6)
		c.grid(column=1,row=2,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(5))
		button.grid(column=2,row=2)

		#`additional_katakana'
		img4 = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","additional_katakana.gif"))
		label = tk.Label(table,image=img4)
		label.grid(column=0,row=3)
		option7 = tk.IntVar()
		option7.set(opt_conv["boolean"][self.param.val('additional_katakana')])
		c = tk.Checkbutton(table,text=str(26),variable=option7)
		c.grid(column=1,row=3,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: portions_popup(6))
		button.grid(column=2,row=3)

		right_frame = tk.Frame(option_frame)
		right_frame.pack(fill="both",expand=1,padx=4)

		#`transcription_system'
		label = tk.Label(right_frame,text=str(61))
		label.pack(fill="both",expand=1)
		option8 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option8,str(62),str(63),str(64),str(79))
		option8.set(opt_conv["transcription_system"][self.param.val('transcription_system')])
		o.pack(fill="both",expand=1)

		#`answer_mode'
		label = tk.Label(right_frame,text=str(38))
		label.pack(fill="both",expand=1)
		option9 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option9,str(39),str(40))
		option9.set(opt_conv["answer_mode"][self.param.val('answer_mode')])
		o.pack(fill="both",expand=1)

		#`list_size'
		label = tk.Label(right_frame,text=str(41))
		label.pack(fill="both",expand=1)
		option10 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option10,str(42) % 2,str(42) % 3,str(42) % 4,str(42) % 5)
		option10.set(opt_conv["list_size"][self.param.val('list_size')])
		o.pack(fill="both",expand=1)
		
		#`rand_answer_sel_range'
		label = tk.Label(right_frame,text=str(75))
		label.pack(fill="both",expand=1)
		option11 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option11,str(76),str(77),str(78))
		option11.set(opt_conv["rand_answer_sel_range"][self.param.val('rand_answer_sel_range')])
		o.pack(fill="both",expand=1)		

		#`length'
		frame2 = tk.Frame(right_frame)
		label = tk.Label(frame2,text=str(43))
		label.pack(side="left",expand=1)
		option12 = tk.StringVar()
		o = tk.OptionMenu(frame2,option12,"10","20","30","40","50")
		option12.set(self.param.val('length'))
		o.pack(side="left",expand=1)
		label = tk.Label(frame2,text=str(80))
		label.pack(expand=1)
		frame2.pack(fill="both",expand=1)

		#`kana_no_repeat'
		option13 = tk.IntVar()
		option13.set(opt_conv["boolean"][self.param.val('kana_no_repeat')])
		c = tk.Checkbutton(right_frame,text=str(44),variable=option13)
		c.pack(fill="both",expand=1)

		#`lang'
		frame2 = tk.Frame(right_frame)
		label = tk.Label(frame2,text=str(45))
		label.pack(side="left",expand=1)
		option14 = tk.StringVar()
		o = tk.OptionMenu(frame2,option14,str(46),str(47),str(70),str(48),str(74),str(49),str(50))
		option14.set(opt_conv["lang"][self.param.val('lang')])
		o.pack(side="left",expand=1)
		frame2.pack(fill="both",expand=1)

		#Buttons at bottom...
		frame2 = tk.Frame(frame)
		frame2.pack(fill="both")
		button = tk.Button(frame2,text=str(51),command=save)
		button.pack(side="left",fill="both",expand=1)
		button = tk.Button(frame2,text=str(52),command=goBack)
		button.pack(side="right",fill="both",expand=1)

		self.window.mainloop() #Without that images aren't displayed! O_o;

	def about(self):
		def close():
			self.dialogState["about"] = 0
			dialog.destroy()
		
		#Check whether this dialog window is not opened yet.
		if not self.dialogState["about"]:
			self.dialogState["about"] = 1

			dialog = tk.Toplevel()
			dialog.resizable(0,0)
			dialog.title(str(4))
			dialog.protocol("WM_DELETE_WINDOW",close)

			frame = tk.Frame(dialog)
			frame.pack(padx=4,pady=4)

			label = tk.Label(frame,text="%s\n %s (Tkinter)\nCopyleft 2003, 2004, 2005, 2006 Choplair-network." % (str(53),str(54) % self.version),fg="#008")
			label.pack()

			label = tk.Label(frame,text=str(55),wraplength=320,justify="left")
			label.pack()

			frame2 = tk.Frame(frame,relief="ridge",borderwidth=1)
			frame2.pack(expand=1,fill="both",pady=4)

			label = tk.Label(frame2,text=str(56),justify="left",anchor="w")
			label.pack(fill="x")

			img = tk.PhotoImage(file=os.path.join(self.datarootpath,"img","chprod.gif"))
			label = tk.Label(frame2,image=img)
			label.pack(side="left")

			label = tk.Label(frame2,text="%s\n\nhttp://www.choplair.org/" % str(57))
			label.pack(side="left",expand=1,fill="x")


			#Button at bottom..
			button = tk.Button(frame,text=str(58),command=close)
			button.pack(side="right")

			self.window.wait_window(dialog)

	def setKanaImage(self,kind,kana):
		"""Update kana image."""
		self.image["file"] = os.path.join(self.datarootpath,"img","kana","%s_%s.gif" % (("k","h")[kind],kana))

	def quit(self):
		self.window.destroy() #Bye~~
