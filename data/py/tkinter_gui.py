"""
Kana no quiz!
Copyleft 2003, 2004, 2005 Choplair-network.

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
import kanaengine, score, i18n

class Gui:
	def __init__(self,options,ver):
		self.param = options
		self.version = ver

		self.window = tk.Tk()
		self.kanaEngine = kanaengine.KanaEngine()
		self.score = score.Score()
		self.dialogState = {"about":0}

		#Localization.
		self.i18n = i18n.I18n()
		self.currentlang = self.param.val('lang')
		self.i18n.setlang(self.param.val('lang'))
		global str
		str = self.i18n.str

		#Initial window attributes.
		self.window.resizable(0,0)

	def main(self,event=None):
		if self.currentlang!=self.param.val('lang'):
			#Change localization...
			self.currentlang = self.param.val('lang')
			self.i18n.setlang(self.param.val('lang'))
			global str
			str = self.i18n.str

		self.window.title(str(0))

		frame = tk.Frame(self.window)
		frame.pack(padx=2,pady=2)

		#Logo
		img = tk.PhotoImage(file="data/img/logo.gif")
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

		self.window.mainloop()

	def intro(self):
		def goBack():
			self.window.slaves()[0].destroy()
			self.main()

		self.window.slaves()[0].destroy()
		self.window.title(str(1)) #Change title of the window.

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
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			(self.param.val('basic_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('contracted_hiragana'),
			self.param.val('basic_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('contracted_katakana'),
			self.param.val('additional_katakana')),
			(self.param.val('basic_hiragana_part'),
			self.param.val('modified_hiragana_part'),
			self.param.val('contracted_hiragana_part'),
			self.param.val('basic_katakana_part'),
			self.param.val('modified_katakana_part'),
			self.param.val('contracted_katakana_part'),
			self.param.val('additional_katakana_part')),
			self.param.val('kana_no_repeat'))

		if self.kana:
			self.window.slaves()[0].destroy()
			frame = tk.Frame(self.window)
			frame.pack(padx=3,pady=3)

			#Display kana image.
			self.image = tk.PhotoImage(file="data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana))
			self.kanaImage = tk.Label(frame,image=self.image)
			self.kanaImage.pack(side="left")

			frame2 = tk.Frame(frame)
			frame2.pack(padx=6,side="right",fill="both")

			self.quizLabel = tk.Label(frame2,text=(str(11),str(12))[self.kanaEngine.getKanaKind()],wraplength=120,width=18)
			self.quizLabel.pack(pady=3,fill="both",expand=1)

			#The arrow.
			self.nextButton = tk.Button(frame2,bitmap="@data/img/rarrow.xbm",pady=4)

			if self.param.val('answer_mode')=="list":
				#Choice buttons generation.
				self.answerButt = {}; i=0
				for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
					if x[-2:]=="-2": x = x[:-2]
					self.answerButt[i] = tk.Button(frame2,text=x.upper(),height=2)
					self.answerButt[i].bind("<ButtonRelease-1>",self.checkAnswer)
					self.answerButt[i].pack(pady=1,fill="both",expand=1)
					i+=1
				self.nextButton['command'] = self.newQuestion
			else:
				self.answerButt = tk.Entry(frame2,width=17)
				self.answerButt.pack()
				self.nextButton['command'] = self.checkAnswer
				self.nextButton.pack(fill="both",pady=1,expand=1)

		else:	tkMessageBox.showwarning(str(61),str(62))

	def checkAnswer(self,event=None):
		"""Check the given answer, update the score
		and display the result."""

		if self.kana[-2:]=="-2": self.kana = self.kana[:-2]

		if self.param.val('answer_mode')=="list": answer = event.widget["text"].lower()
		else: answer = self.answerButt.get().lower()

		if answer==self.kana:
			self.quizLabel["text"] = str(13)
			self.quizLabel["fg"] = "darkgreen"
			self.score.update(1) #Update the score (add 1 point).
		else:
			self.quizLabel["text"] = "%s\n%s" % (str(14), str(15) % self.kana.upper())
			self.quizLabel["fg"] = "red"
			self.score.update() #Update the score.

		if self.param.val('answer_mode')=="list":
			for butt in self.answerButt.values(): butt.pack_forget() #Hide choices buttons.
			self.nextButton.pack(fill="both",pady=1,expand=1)
		else:
			self.answerButt.pack_forget()
			self.nextButton['command'] = self.newQuestion

		if self.score.isQuizFinished(self.param.val('length')):
			#The quiz is finished... Let's show results!
			self.nextButton["command"]  = self.results

	def newQuestion(self):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			(self.param.val('basic_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('contracted_hiragana'),
			self.param.val('basic_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('contracted_katakana'),
			self.param.val('additional_katakana')),
			(self.param.val('basic_hiragana_part'),
			self.param.val('modified_hiragana_part'),
			self.param.val('contracted_hiragana_part'),
			self.param.val('basic_katakana_part'),
			self.param.val('modified_katakana_part'),
			self.param.val('contracted_katakana_part'),
			self.param.val('additional_katakana_part')),
			self.param.val('kana_no_repeat')) 

		self.image["file"] = "data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana) #Update kana's image.

		self.quizLabel["text"] = (str(11),str(12))[self.kanaEngine.getKanaKind()]
		self.quizLabel["fg"] = "black"

		if self.param.val('answer_mode')=="list":
			self.nextButton.pack_forget() #Hide the arrow.
			#Display the random list.
			i=0
			for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
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

	def results(self):
		def goBack():
			self.window.slaves()[0].pack_forget()
			self.main()

		#Display results.
		self.quizLabel["text"] = ("%s\n\n%s\n%s\n%s" % (str(16),str(17) % self.score.getResults()[0],str(18) % self.score.getResults()[1],str(19) % self.score.getResults()[2]))
		self.quizLabel["fg"] = "black"

		self.nextButton["command"] = goBack

		self.score.reset() #Reset the score.

	def options(self):
		#Dicts for integrer to string options convertion and vice-versa...
		opt_boolean = {0:'false',1:'true','false':0,'true':1}
		opt_answer_mode = {str(39):'list',str(40):'entry','list':str(39),'entry':str(40)}
		opt_list_size = {str(42):2,str(43):3,str(44):4,2:str(42),3:str(43),4:str(44)}
		opt_lang = {str(48):'en',str(49):'fr',str(50):'pt_BR',str(51):'sv',str(62):'sr','en':str(48),'fr':str(49),'pt_BR':str(50),'sv':str(51),'sr':str(62)}

		#Values for kana part params.
		kanaParts = [
			self.param.val('basic_hiragana_part'),
			self.param.val('modified_hiragana_part'),
			self.param.val('contracted_hiragana_part'),
			self.param.val('basic_katakana_part'),
			self.param.val('modified_katakana_part'),
			self.param.val('contracted_katakana_part'),
			self.param.val('additional_katakana_part')]

		def goBack():
			self.window.slaves()[0].destroy()
			self.main()

		def save():
			self.param.write({
			'basic_hiragana':opt_boolean[option1.get()],
			'basic_hiragana_part':kanaParts[0],
			'modified_hiragana':opt_boolean[option2.get()],
			'modified_hiragana_part':kanaParts[1],
			'contracted_hiragana':opt_boolean[option3.get()],
			'contracted_hiragana_part':kanaParts[2],
			'basic_katakana':opt_boolean[option4.get()],
			'basic_katakana_part':kanaParts[3],
			'modified_katakana':opt_boolean[option5.get()],
			'modified_katakana_part':kanaParts[4],
			'contracted_katakana':opt_boolean[option6.get()],
			'contracted_katakana_part':kanaParts[5],
			'additional_katakana':opt_boolean[option7.get()],
			'additional_katakana_part':kanaParts[6],
			'answer_mode':opt_answer_mode[option8.get().encode('utf8')],
			'list_size':opt_list_size[option9.get().encode('utf8')],
			'length':int(option10.get()),
			'kana_no_repeat':opt_boolean[option11.get()],
			'lang':opt_lang[option12.get().encode('utf8')]
			})
			goBack() #Then, go back!

		def parts_popup(kanaset):
			def close():
				self.dialogState["about"] = 0
				dialog.destroy()

			def validedChanges():
				kanaParts[kanaset] = self.temp_value.get()
				close()

			#Check whether this dialog window is not opened yet.
			if not self.dialogState["about"]:
				self.dialogState["about"] = 1

				#Temporary variable.
				self.temp_value = tk.IntVar()
				self.temp_value.set(kanaParts[kanaset])

				dialog = tk.Toplevel()
				dialog.resizable(0,0)
				dialog.title(str(28+kanaset))
				dialog.protocol("WM_DELETE_WINDOW",close)

				label = tk.Label(dialog,text=str(35),wraplength=350)
				label.pack()

				label = tk.Label(dialog,text=str(36),wraplength=350)
				label.pack()

				table = tk.Frame(dialog)
				table.pack()

				radio0 = tk.Radiobutton(table,text=str(37),variable=self.temp_value,value=0)
				radio0.grid(column=0,row=0)
				
				set = self.kanaEngine.getASet(kanaset)
				i,j,k = 1,1,0
				for part in set:
					string = ""
					for kana in part: string += "%s " % kana.upper()
					radio = tk.Radiobutton(table,text=string[:-1],variable=self.temp_value,value=i)
					if kanaParts[kanaset]==i: radio.select()
					if j: radio.grid(column=1,row=k); j=0; k+=1
					else: radio.grid(column=0,row=k); j=1
					i+=1

				#Buttons at bottom..
				button = tk.Button(dialog,text=str(59),command=close)
				button.pack(side="right")
				button = tk.Button(dialog,text=str(10),command=validedChanges)
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
		left_frame.pack(fill="both",expand=1,side="left",pady=4,padx=4)

		frame2 = tk.Frame(left_frame,relief="ridge",borderwidth=1)
		frame2.pack(fill="both",expand=1)

		label = tk.Label(frame2,text=str(21),justify="left",anchor="w")
		label.pack()

		table = tk.Frame(frame2)
		table.pack(fill="x")

		#`basic_hiragana'
		img5 = tk.PhotoImage(file="data/img/basic_hiragana.gif")
		label = tk.Label(table,image=img5)
		label.grid(column=0,row=0)
		option1 = tk.IntVar()
		option1.set(opt_boolean[self.param.val('basic_hiragana')])
		c = tk.Checkbutton(table,text=str(23),variable=option1)
		c.grid(column=1,row=0,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(0))
		button.grid(column=2,row=0)

		#`modified_hiragana'
		img6 = tk.PhotoImage(file="data/img/modified_hiragana.gif")
		label = tk.Label(table,image=img6)
		label.grid(column=0,row=1)
		option2 = tk.IntVar()
		option2.set(opt_boolean[self.param.val('modified_hiragana')])
		c = tk.Checkbutton(table,text=str(24),variable=option2)
		c.grid(column=1,row=1,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(1))
		button.grid(column=2,row=1)

		#`contracted_hiragana'
		img7 = tk.PhotoImage(file="data/img/contracted_hiragana.gif")
		label = tk.Label(table,image=img7)
		label.grid(column=0,row=2)
		option3 = tk.IntVar()
		option3.set(opt_boolean[self.param.val('contracted_hiragana')])
		c = tk.Checkbutton(table,text=str(25),variable=option3)
		c.grid(column=1,row=2,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(2))
		button.grid(column=2,row=2)

		frame2 = tk.Frame(left_frame,relief="ridge",borderwidth=1)
		frame2.pack(fill="both",expand=1)

		label = tk.Label(frame2,text=str(22),justify="left",anchor="w")
		label.pack()

		table = tk.Frame(frame2)
		table.pack(fill="x")

		#`basic_katakana'
		img1 = tk.PhotoImage(file="data/img/basic_katakana.gif")
		label = tk.Label(table,image=img1)
		label.grid(column=0,row=0)
		option4 = tk.IntVar()
		option4.set(opt_boolean[self.param.val('basic_katakana')])
		c = tk.Checkbutton(table,text=str(23),variable=option4)
		c.grid(column=1,row=0,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(3))
		button.grid(column=2,row=0)

		#`modified_katakana'
		img2 = tk.PhotoImage(file="data/img/modified_katakana.gif")
		label = tk.Label(table,image=img2)
		label.grid(column=0,row=1)
		option5 = tk.IntVar()
		option5.set(opt_boolean[self.param.val('modified_katakana')])
		c = tk.Checkbutton(table,text=str(24),variable=option5)
		c.grid(column=1,row=1,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(4))
		button.grid(column=2,row=1)

		#`contracted_katakana'
		img3 = tk.PhotoImage(file="data/img/contracted_katakana.gif")
		label = tk.Label(table,image=img3)
		label.grid(column=0,row=2)
		option6 = tk.IntVar()
		option6.set(opt_boolean[self.param.val('contracted_katakana')])
		c = tk.Checkbutton(table,text=str(25),variable=option6)
		c.grid(column=1,row=2,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(5))
		button.grid(column=2,row=2)

		#`additional_katakana'
		img4 = tk.PhotoImage(file="data/img/additional_katakana.gif")
		label = tk.Label(table,image=img4)
		label.grid(column=0,row=3)
		option7 = tk.IntVar()
		option7.set(opt_boolean[self.param.val('additional_katakana')])
		c = tk.Checkbutton(table,text=str(26),variable=option7)
		c.grid(column=1,row=3,sticky='W')
		button = tk.Button(table,text=str(27),command=lambda: parts_popup(6))
		button.grid(column=2,row=3)

		right_frame = tk.Frame(option_frame)
		right_frame.pack(fill="both",expand=1,pady=6,padx=6)

		#`answer_mode'
		label = tk.Label(right_frame,text=str(38))
		label.pack(fill="both",expand=1)
		option8 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option8,str(39),str(40))
		option8.set(opt_answer_mode[self.param.val('answer_mode')])
		o.pack(fill="both",expand=1)

		#`list_size'
		label = tk.Label(right_frame,text=str(41))
		label.pack(fill="both",expand=1)
		option9 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option9,str(42),str(43),str(44))
		option9.set(opt_list_size[self.param.val('list_size')])
		o.pack(fill="both",expand=1)

		#`length'
		frame2 = tk.Frame(right_frame)
		label = tk.Label(frame2,text=str(45))
		label.pack(side="left",expand=1)
		option10 = tk.StringVar()
		o = tk.OptionMenu(frame2,option10,"10","20","30")
		option10.set(self.param.val('length'))
		o.pack(expand=1)
		frame2.pack(fill="both",expand=1)

		#`kana_no_repeat'
		option11 = tk.IntVar()
		option11.set(opt_boolean[self.param.val('kana_no_repeat')])
		c = tk.Checkbutton(right_frame,text=str(46),variable=option11)
		c.pack(fill="both",expand=1)

		#`lang'
		label = tk.Label(right_frame,text=str(47))
		label.pack(fill="both",expand=1)
		option12 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option12,str(48),str(49),str(50),str(62),str(51))
		option12.set(opt_lang[self.param.val('lang')])
		o.pack(fill="both",expand=1)

		#Buttons at bottom...
		frame2 = tk.Frame(frame)
		frame2.pack(fill="both")
		button = tk.Button(frame2,text=str(52),command=save)
		button.pack(side="left",fill="both",expand=1)
		button = tk.Button(frame2,text=str(53),command=goBack)
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
			dialog.title(str(3))
			dialog.protocol("WM_DELETE_WINDOW",close)

			frame = tk.Frame(dialog)
			frame.pack(padx=4,pady=4)

			label = tk.Label(frame,text="%s\n (Tkinter)%s\nCopyleft 2003, 2004, 2005 Choplair-network." % (str(54),str(55) % self.version),fg="#008")
			label.pack()

			label = tk.Label(frame,text=str(56),wraplength=320,justify="left")
			label.pack()

			frame2 = tk.Frame(frame,relief="ridge",borderwidth=1)
			frame2.pack(expand=1,fill="both",pady=4)

			label = tk.Label(frame2,text=str(57),justify="left",anchor="w")
			label.pack(fill="x")

			img = tk.PhotoImage(file="data/img/chprod.gif")
			label = tk.Label(frame2,image=img)
			label.pack(side="left")

			label = tk.Label(frame2,text="%s\n\nhttp://www.choplair.org/" % str(58))
			label.pack(side="left",expand=1,fill="x")

			#Button at bottom..
			button = tk.Button(frame,text=str(59),command=close)
			button.pack(side="right")

			self.window.wait_window(dialog)
