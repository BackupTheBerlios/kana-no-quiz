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
# This is Tkinter interface, mainly designed for windows user.

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
		label.pack()

		frame2 = tk.Frame(frame)
		frame2.pack(fill="both")
		button = tk.Button(frame2,text=str(1),command=self.quiz)
		button.pack(side="left",fill="both",expand=1)
		button = tk.Button(frame2,text=str(2),command=self.options)
		button.pack(side="left",fill="both",expand=1)
		button = tk.Button(frame2,text=str(3),command=self.about)
		button.pack(side="right",fill="both",expand=1)

		self.window.mainloop()

	def quiz(self):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			self.param.val('single_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('combined_katakana'),
			self.param.val('single_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('combined_hiragana'))

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
	
			self.quizLabel = tk.Label(frame2,text=(str(4),str(5))[self.kanaEngine.getKanaKind()],wraplength=120,width=18)
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
	
		else:	tkMessageBox.showwarning(str(44),str(45))

	def checkAnswer(self,event=None):
		"""Check the given answer, update the score
		and display the result."""

		if self.kana[-2:]=="-2": self.kana = self.kana[:-2]

		if self.param.val('answer_mode')=="list": answer = event.widget["text"].lower()
		else: answer = self.answerButt.get().lower()

		if answer==self.kana:
			self.quizLabel["text"] = str(6)
			self.quizLabel["fg"] = "darkgreen"
			self.score.update(1) #Update the score (add 1 point).
		else:
			self.quizLabel["text"] = "%s\n%s" % (str(7), str(8) % self.kana.upper())
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
			self.param.val('single_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('combined_katakana'),
			self.param.val('single_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('combined_hiragana'))

		self.image["file"] = "data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana) #Update kana's image.

		self.quizLabel["text"] = (str(4),str(5))[self.kanaEngine.getKanaKind()]
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
		self.quizLabel["text"] = ("%s\n\n%s\n%s\n%s" % (str(9),str(10) % self.score.getResults()[0],str(11) % self.score.getResults()[1],str(12) % self.score.getResults()[2]))
		self.quizLabel["fg"] = "black"

		self.nextButton["command"] = goBack

		self.score.reset() #Reset the score.

	def options(self):
		#Dicts for integrer to string options convertion and vice-versa...
		opt_boolean = {0:'false',1:'true','false':0,'true':1}
		opt_answer_mode = {str(24):'list',str(25):'entry','list':str(24),'entry':str(25)}
		opt_list_size = {str(27):'2',str(28):'3',str(29):'4','2':str(27),'3':str(28),'4':str(29)}
		opt_length = {str(20):'short',str(21):'normal',str(22):'long','short':str(20),'normal':str(21),'long':str(22)}
		opt_lang = {str(31):'en',str(32):'fr',str(34):'sv','en':str(31),'fr':str(32),'sv':str(34)}

		def save():
			self.param.write({
			'single_katakana':opt_boolean[option1.get()],
			'modified_katakana':opt_boolean[option2.get()],
			'combined_katakana':opt_boolean[option3.get()],
			'extended_katakana':opt_boolean[option4.get()],
			'single_hiragana':opt_boolean[option5.get()],
			'modified_hiragana':opt_boolean[option6.get()],
			'combined_hiragana':opt_boolean[option7.get()],
			'answer_mode':opt_answer_mode[option8.get().encode('utf8')],
			'list_size':opt_list_size[option9.get().encode('utf8')],
			'length':opt_length[option10.get().encode('utf8')],
			'lang':opt_lang[option11.get().encode('utf8')]
			})
			goBack() #Then, go back!

		def goBack():
			self.window.slaves()[0].destroy()
			self.main()

		self.window.slaves()[0].destroy()
		self.window.title(str(2)) #Change title of window.

		frame = tk.Frame(self.window)
		frame.pack(padx=2,pady=2)

		label = tk.Label(frame,text=str(13))
		label.pack()

		option_frame = tk.Frame(frame)
		option_frame.pack(fill="both",expand=1)

		left_frame = tk.Frame(option_frame)
		left_frame.pack(fill="both",expand=1,side="left",pady=4,padx=4)

		frame2 = tk.Frame(left_frame,relief="ridge",borderwidth=1)
		frame2.pack(fill="both",expand=1)

		label = tk.Label(frame2,text=str(14),justify="left",anchor="w")
		label.pack()

		table = tk.Frame(frame2)
		table.pack(fill="x")

		#`single_katakana'
		img1 = tk.PhotoImage(file="data/img/single_katakana.gif")
		label = tk.Label(table,image=img1)
		label.grid(column=0,row=0)
		option1 = tk.IntVar()
		option1.set(opt_boolean[self.param.val('single_katakana')])
		c = tk.Checkbutton(table,text=str(16),variable=option1)
		c.grid(column=1,row=0)

		#`modified_katakana'
		img2 = tk.PhotoImage(file="data/img/modified_katakana.gif")
		label = tk.Label(table,image=img2)
		label.grid(column=0,row=1)
		option2 = tk.IntVar()
		option2.set(opt_boolean[self.param.val('modified_katakana')])
		c = tk.Checkbutton(table,text=str(17),variable=option2)
		c.grid(column=1,row=1)

		#`combined_katakana'
		img3 = tk.PhotoImage(file="data/img/combined_katakana.gif")
		label = tk.Label(table,image=img3)
		label.grid(column=0,row=2)
		option3 = tk.IntVar()
		option3.set(opt_boolean[self.param.val('combined_katakana')])
		c = tk.Checkbutton(table,text=str(18),variable=option3)
		c.grid(column=1,row=2)

		#`extended_katakana'
		img4 = tk.PhotoImage(file="data/img/extended_katakana.gif")
		label = tk.Label(table,image=img4)
		label.grid(column=0,row=3)
		option4 = tk.IntVar()
		option4.set(opt_boolean[self.param.val('extended_katakana')])
		c = tk.Checkbutton(table,text=str(19),variable=option4)
		c.grid(column=1,row=3)

		frame2 = tk.Frame(left_frame,relief="ridge",borderwidth=1)
		frame2.pack(fill="both",expand=1)

		label = tk.Label(frame2,text=str(15),justify="left",anchor="w")
		label.pack()

		table = tk.Frame(frame2)
		table.pack(fill="x")

		#`single_hiragana'
		img5 = tk.PhotoImage(file="data/img/single_hiragana.gif")
		label = tk.Label(table,image=img5)
		label.grid(column=0,row=0)
		option5 = tk.IntVar()
		option5.set(opt_boolean[self.param.val('single_hiragana')])
		c = tk.Checkbutton(table,text=str(16),variable=option5)
		c.grid(column=1,row=0)

		#`modified_hiragana'
		img6 = tk.PhotoImage(file="data/img/modified_hiragana.gif")
		label = tk.Label(table,image=img6)
		label.grid(column=0,row=1)
		option6 = tk.IntVar()
		option6.set(opt_boolean[self.param.val('modified_hiragana')])
		c = tk.Checkbutton(table,text=str(17),variable=option6)
		c.grid(column=1,row=1)

		#`combined_hiragana'
		img7 = tk.PhotoImage(file="data/img/combined_hiragana.gif")
		label = tk.Label(table,image=img7)
		label.grid(column=0,row=2)
		option7 = tk.IntVar()
		option7.set(opt_boolean[self.param.val('combined_hiragana')])
		c = tk.Checkbutton(table,text=str(18),variable=option7)
		c.grid(column=1,row=2)

		right_frame = tk.Frame(option_frame)
		right_frame.pack(fill="both",expand=1,pady=6,padx=6)

		#`answer_mode'
		label = tk.Label(right_frame,text=str(20))
		label.pack(fill="both",expand=1)
		option8 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option8,str(21),str(22))
		option8.set(opt_answer_mode[self.param.val('answer_mode')])
		o.pack(fill="both",expand=1)

		#`list_size'
		label = tk.Label(right_frame,text=str(23))
		label.pack(fill="both",expand=1)
		option9 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option9,str(24),str(25),str(26))
		option9.set(opt_list_size[self.param.val('list_size')])
		o.pack(fill="both",expand=1)

		#`length'
		label = tk.Label(right_frame,text=str(27))
		label.pack(fill="both",expand=1)
		option10 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option10,str(28),str(29),str(30))
		option10.set(opt_length[self.param.val('length')])
		o.pack(fill="both",expand=1)

		#`lang'
		label = tk.Label(right_frame,text=str(31))
		label.pack(fill="both",expand=1)
		option11 = tk.StringVar()
		o = tk.OptionMenu(right_frame,option11,str(32),str(33),str(35))
		option11.set(opt_lang[self.param.val('lang')])
		o.pack(fill="both",expand=1)

		#Buttons at bottom...
		frame2 = tk.Frame(frame)
		frame2.pack(fill="both")
		button = tk.Button(frame2,text=str(36),command=save)
		button.pack(side="left",fill="both",expand=1)
		button = tk.Button(frame2,text=str(37),command=goBack)
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

			label = tk.Label(frame,text="%s\n%s\nCopyleft 2003, 2004 Choplair-network." % (str(38),str(39) % self.version),fg="#008")
			label.pack()

			label = tk.Label(frame,text=str(40),wraplength=320,justify="left")
			label.pack()

			frame2 = tk.Frame(frame,relief="ridge",borderwidth=1)
			frame2.pack(expand=1,fill="both",pady=4)

			label = tk.Label(frame2,text=str(41),justify="left",anchor="w")
			label.pack(fill="x")
	
			img = tk.PhotoImage(file="data/img/chprod.gif")
			label = tk.Label(frame2,image=img)
			label.pack(side="left")

			label = tk.Label(frame2,text="%s\n\nhttp://www.choplair.org/" % str(42))
			label.pack(side="left",expand=1,fill="x")

			#Button at bottom..
			button = tk.Button(frame,text=str(43),command=close)
			button.pack(side="right")

			self.window.wait_window(dialog)
