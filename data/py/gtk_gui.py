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
import gtk
import kanaengine, score, i18n

class Gui:
	def __init__(self,options,ver):
		self.param = options
		self.version = ver

		self.window = gtk.Window()
		self.kanaEngine =  kanaengine.KanaEngine()
		self.score = score.Score()
		self.dialogState = {"about":0,"options":0}

		#Localization.
		self.i18n = i18n.I18n()
		self.currentlang = self.param.val('lang')
		self.i18n.setlang(self.param.val('lang'))
		global str
		str = self.i18n.str

		#Initial window attributes.
		self.window.set_title(str(0))
		self.window.connect("destroy",self.quit)
		self.window.set_border_width(5)

	def main(self,oldbox=None):
		if self.currentlang!=self.param.val('lang'):
			#Change localization...
			self.currentlang = self.param.val('lang')
			self.i18n.setlang(self.param.val('lang'))
			global str
			str = self.i18n.str
		
		if oldbox: self.window.resize(1,1) #Properly resize the window.

		box = gtk.VBox()
		image = gtk.Image()
		image.set_from_file("data/img/logo.gif")
		box.pack_start(image,gtk.FALSE)
		box2 = gtk.HBox()
		box2.set_size_request(-1,35)
		button = gtk.Button(str(1))
		button.connect_object("clicked",self.quiz,box)
		box2.pack_start(button)
		button = gtk.Button(str(2))
		button.connect_object("clicked",self.options,box)
		box2.pack_start(button)
		button = gtk.Button(str(3))
		button.connect("clicked",self.about)
		box2.pack_start(button)
		box.pack_start(box2)

		if oldbox: self.window.remove(oldbox)
		self.window.add(box)
		self.window.show_all()

		#Initialize pyGTK if it haven't been done yet.
		if not oldbox : gtk.main()

	def quiz(self,oldbox):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			self.param.val('single_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('combined_katakana'),
			self.param.val('single_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('combined_hiragana'))

		if self.kana:
			box = gtk.HBox(spacing=4)
	
			#Display kana image.
			self.kanaImage = gtk.Image()
			self.kanaImage.set_from_file("data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana))
			box.pack_start(self.kanaImage,gtk.FALSE)
	
			box2 = gtk.VBox(spacing=4)
	
			self.quizLabel = gtk.Label((str(4),str(5))[self.kanaEngine.getKanaKind()])
			self.quizLabel.set_justify(gtk.JUSTIFY_CENTER)
			self.quizLabel.set_line_wrap(gtk.TRUE)
			box2.pack_start(self.quizLabel)
	
			#Choice buttons generation.
			self.answerButt = {}; i=0
			for x in self.kanaEngine.randomAnswers(self.param.val('difficulty')):
				if x[-2:]=="-2": x = x[:-2]
				self.answerButt[i] = gtk.Button(x.upper())
				self.answerButt[i].connect("clicked",self.checkAnswer)
				box2.pack_start(self.answerButt[i])
				i+=1
	
			arrow = gtk.Arrow(gtk.ARROW_RIGHT,gtk.SHADOW_IN)
			self.nextButton = gtk.Button()
			self.nextButton.add(arrow)
			self.handlerid = self.nextButton.connect("clicked",self.newQuestion)
			box2.pack_start(self.nextButton)
			box.pack_end(box2)
	
			#Forget the old box
			self.window.remove(oldbox)
			#Then add the new one
			self.window.add(box)
			self.window.show_all()
	
			self.nextButton.hide() #Hide the arrow.

		else:	
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING,gtk.BUTTONS_OK,str(40))
			dialog.set_title(str(39))
			dialog.connect('response', lambda dialog, response: dialog.destroy())
			dialog.show()

	def checkAnswer(self,widget):
		"""Check the given answer, display result, and
		update the score."""

		if self.kana[-2:]=="-2": self.kana = self.kana[:-2]
		
		if widget.get_label().lower()==self.kana: 
			self.quizLabel.set_text("<span color='darkgreen'><b>%s</b></span>" % str(6))
			self.score.update(1) #Update the score (add 1 point).
		else:
			self.quizLabel.set_text("<span color='red'><b>%s</b></span>\n%s" % (str(7),str(8) % "<b>%s</b>" % self.kana.upper()))
			self.score.update() #Update the score.
		self.quizLabel.set_use_markup(gtk.TRUE)

		self.nextButton.show() #Show the arrow.
		for butt in self.answerButt.values(): butt.hide() #Hide choices buttons.

		if self.score.isQuizFinished(self.param.val('length')):
			#The quiz is finished... Let's show results!
			self.nextButton.disconnect(self.handlerid)
			self.handlerid = self.nextButton.connect("clicked",self.results)

	def newQuestion(self,widget):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			self.param.val('single_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('combined_katakana'),
			self.param.val('single_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('combined_hiragana'))

		self.kanaImage.set_from_file("data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana)) #Update kana's image

		self.quizLabel.set_text((str(4),str(5))[self.kanaEngine.getKanaKind()])

		self.nextButton.hide() #Hide the arrow.

		i=0
		for x in self.kanaEngine.randomAnswers(self.param.val('difficulty')):
			if x[-2:]=="-2": x = x[:-2]
			self.answerButt[i].set_label(x.upper())
			self.answerButt[i].show()
			i+=1
	
	def results(self,data):
		#Display results.
		self.quizLabel.set_text("<big>%s</big>\n\n%s\n%s\n%s" % (str(9),str(10) % self.score.getResults()[0],str(11) % self.score.getResults()[1],str(12) % self.score.getResults()[2]))
		self.quizLabel.set_use_markup(gtk.TRUE)

		self.score.reset() #Reset the score.
		self.kanaImage.hide() #Hide kana image.

		#Connect the arrow to the "main".
		self.nextButton.disconnect(self.handlerid)
		self.nextButton.connect_object("clicked",self.main,self.window.get_child())

	def options(self,oldbox):
		#Dicts for integrer to string options convertion and vice-versa...
		opt_question_set = {0:'false',1:'true','false':0,'true':1}
		opt_length = {0:'short',1:'normal',2:'long','short':0,'normal':1,'long':2}
		opt_difficulty = {0:'novice',1:'medium',2:'sensei','novice':0,'medium':1,'sensei':2}
		opt_lang = {0:'en',1:'fr',2:'sv','en':0,'fr':1,'sv':2}

		def callback(widget,special=None):
			if special=="save":
				#Update the configuration.
				self.param.write({
				'single_katakana':opt_question_set[option1.get_active()],
				'modified_katakana':opt_question_set[option2.get_active()],
				'combined_katakana':opt_question_set[option3.get_active()],
				'single_hiragana':opt_question_set[option4.get_active()],
				'modified_hiragana':opt_question_set[option5.get_active()],
				'combined_hiragana':opt_question_set[option6.get_active()],
				'length':opt_length[option7.get_history()],
				'difficulty':opt_difficulty[option8.get_history()],
				'lang':opt_lang[option9.get_history()]
				})
			self.main(box) #Go back to the "main".

		self.window.set_title(str(2)) #Change title of window.
		box = gtk.VBox(spacing=4)

		label = gtk.Label(str(13))
		box.pack_start(label,gtk.FALSE)

		frame = gtk.Frame(str(14))
		box.pack_start(frame)
		box2 = gtk.HBox(spacing=5)
		box2.set_border_width(3)
		frame.add(box2)

		#`single_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/single_katakana.gif")
		box2.pack_start(image)
		option1 = gtk.CheckButton(str(16))
		option1.set_active(opt_question_set[self.param.val('single_katakana')])
		box2.pack_start(option1)
		
		#`modified_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/modified_katakana.gif")
		box2.pack_start(image)
		option2 = gtk.CheckButton(str(17))
		option2.set_active(opt_question_set[self.param.val('modified_katakana')])
		box2.pack_start(option2)

		#`combined_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/combined_katakana.gif")
		box2.pack_start(image)
		option3 = gtk.CheckButton(str(18))
		option3.set_active(opt_question_set[self.param.val('combined_katakana')])
		box2.pack_start(option3)

		frame = gtk.Frame(str(15))
		box.pack_start(frame)
		box2 = gtk.HBox(spacing=5)
		box2.set_border_width(3)
		frame.add(box2)

		#`single_hiragana'
		image = gtk.Image()
		image.set_from_file("data/img/single_hiragana.gif")
		box2.pack_start(image)
		option4 = gtk.CheckButton(str(16))
		option4.set_active(opt_question_set[self.param.val('single_hiragana')])
		box2.pack_start(option4)
		
		#`modified_hiragana'
		image = gtk.Image()
		image.set_from_file("data/img/modified_hiragana.gif")
		box2.pack_start(image)
		option5 = gtk.CheckButton(str(17))
		option5.set_active(opt_question_set[self.param.val('modified_hiragana')])
		box2.pack_start(option5)

		#`combined_hiragana'
		image = gtk.Image()
		image.set_from_file("data/img/combined_hiragana.gif")
		box2.pack_start(image)
		option6 = gtk.CheckButton(str(18))
		option6.set_active(opt_question_set[self.param.val('combined_hiragana')])
		box2.pack_start(option6)

		table = gtk.Table(2,3)
		table.set_row_spacings(3)

		#`length'
		label = gtk.Label(str(19))
		table.attach(label,0,1,1,2)
		menu = gtk.Menu()
		for val in (str(20),str(21),str(22)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option7 = gtk.OptionMenu()
		option7.set_menu(menu)
		option7.set_history(opt_length[self.param.val('length')])
		table.attach(option7,1,2,1,2)

		#`difficulty'
		label = gtk.Label(str(23))
		table.attach(label,0,1,2,3)
		menu = gtk.Menu()
		for val in (str(24),str(25),str(26)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option8 = gtk.OptionMenu()
		option8.set_menu(menu)
		option8.set_history(opt_difficulty[self.param.val('difficulty')])
		table.attach(option8,1,2,2,3)

		#`lang'
		label = gtk.Label(str(27))
		table.attach(label,0,1,3,4)
		menu = gtk.Menu()
		for val in (str(28),str(29),str(30)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option9 = gtk.OptionMenu()
		option9.set_menu(menu)
		option9.set_history(opt_lang[self.param.val('lang')])
		table.attach(option9,1,2,3,4)

		box.pack_start(table)

		#Buttons at bottom...
		box2 = gtk.HBox()
		box2.set_size_request(-1,35)
		button = gtk.Button(stock=gtk.STOCK_SAVE)
		button.connect("clicked",callback,"save")
		box2.pack_start(button)
		button = gtk.Button(stock=gtk.STOCK_CANCEL)
		button.connect("clicked",callback)
		box2.pack_start(button)
		box.pack_end(box2,gtk.FALSE)

		#Remove the old box then add the new one.
		self.window.remove(oldbox)
		self.window.add(box)

		self.window.show_all()

	def about(self,widget):
		#Check whether this dialog window is not opened yet.
		if not self.dialogState["about"]:
			self.dialogState["about"] = 1

			dialog = gtk.Dialog(str(3),flags=gtk.DIALOG_NO_SEPARATOR)
			dialog.connect("destroy",self.destroy,"about")

			#Border and spacing...
			dialog.set_border_width(5)
			dialog.vbox.set_spacing(5)

			label = gtk.Label("<span color='#008'><b>%s</b>\n%s\nCopyleft 2003, 2004 Choplair-network.</span>" % (str(33),str(34) % self.version))
			label.set_justify(gtk.JUSTIFY_CENTER)
			label.set_use_markup(gtk.TRUE)
			dialog.vbox.pack_start(label)

			label = gtk.Label(str(35))
			label.set_line_wrap(gtk.TRUE)
			dialog.vbox.pack_start(label)

			frame = gtk.Frame(str(36))
			box = gtk.HBox()

			logo = gtk.Image()
			logo.set_from_file("data/img/chprod.png")
			box.pack_start(logo,gtk.FALSE)

			label = gtk.Label("%s\n\nhttp://www.choplair.org/" % str(37))
			label.set_justify(gtk.JUSTIFY_CENTER)
			box.pack_start(label)

			frame.add(box)
			dialog.vbox.pack_start(frame)

			#Button at bottom..
			button = gtk.Button(stock=gtk.STOCK_CLOSE)
			button.connect_object("clicked",self.destroy,dialog)
			dialog.action_area.pack_end(button)

			dialog.show_all()

	def destroy(self,widget,data=None):
		widget.destroy() #Emit destroy signal.
		if data: self.dialogState[data] = 0 #State chagement.

	def quit(self,widget):
		gtk.main_quit() #Bye~~
