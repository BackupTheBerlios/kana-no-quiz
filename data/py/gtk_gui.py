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
		self.dialogState = {"about":0}

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

		if oldbox: 
			self.window.set_title(str(0))
			self.window.resize(1,1) #Properly resize the window.

		box = gtk.HBox()

		image = gtk.Image()
		image.set_from_file("data/img/logo.gif")
		box.pack_start(image,gtk.FALSE)

		box2 = gtk.VBox()
		button = gtk.Button(str(1))
		button.connect_object("clicked",self.intro,box)
		box2.pack_start(button)
		button = gtk.Button(str(2))
		button.connect_object("clicked",self.options,box)
		box2.pack_start(button)
		button = gtk.Button(str(3))
		button.connect_object("clicked",self.quiz,box)
		box2.pack_start(button)
		button = gtk.Button(str(4))
		button.connect("clicked",self.about)
		box2.pack_start(button)
		box.pack_start(box2)

		if oldbox: self.window.remove(oldbox)
		self.window.add(box)
		self.window.show_all()

		#Initialize pyGTK if it haven't been done yet.
		if not oldbox : gtk.main()

	def intro(self,oldbox):
		#Here comes the marvelous introduction...
		self.window.set_title(str(1)) #Change title of window.
		box = gtk.VBox(spacing=5)
	
		label = gtk.Label("Two different writing systems are commonly used by Japaneses: <b>Kanji</b> &amp; <b>Kana</b>.")
		label.set_line_wrap(gtk.TRUE)
		box.pack_start(label)
		label.set_use_markup(gtk.TRUE)

		label = gtk.Label("Kanji are complex ideograms retranscribing words whereas Kana are simple symbols used as syllabes which have to be combined to make words. Any word in Japanese can be written using Kana.")
		label.set_line_wrap(gtk.TRUE)
		label.set_use_markup(gtk.TRUE)
		box.pack_start(label)

		label = gtk.Label("There are two kinds of Kana: <b>Hiragana</b> &amp; <b>Katakana</b>. Hiragana is the most-used traditional syllabary used to write Japanese words. Katakana is a larger syllabary mostly used to write proper nouns and words of foreign origin.")
		label.set_line_wrap(gtk.TRUE)
		label.set_use_markup(gtk.TRUE)
		box.pack_start(label)

		label = gtk.Label("<b>Kana no quiz</b> help you to memorize Kana and their associated roman transcription (<b>Hepburn</b> system). For more simplicity, syllabes have been splited in multiple sets, and you can even choose to learn only a portion of Kana at a time.")
		label.set_line_wrap(gtk.TRUE)
		label.set_use_markup(gtk.TRUE)
		box.pack_start(label)

		label = gtk.Label("Have a good practice !")
		box.pack_start(label)

		button = gtk.Button(stock=gtk.STOCK_OK)
		button.connect_object("clicked",self.main,box)
		box.pack_end(button)

		#Forget the old box
		self.window.remove(oldbox)
		#Then add the new one
		self.window.add(box)
		self.window.show_all()

	def quiz(self,oldbox):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			self.param.val('basic_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('contracted_katakana'),
			self.param.val('additional_katakana'),
			self.param.val('basic_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('contracted_hiragana'))

		if self.kana:
			box = gtk.HBox(spacing=4)
	
			#Display kana image.
			self.kanaImage = gtk.Image()
			self.kanaImage.set_from_file("data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana))
			box.pack_start(self.kanaImage,gtk.FALSE)
	
			box2 = gtk.VBox(spacing=4)
	
			self.quizLabel = gtk.Label((str(5),str(6))[self.kanaEngine.getKanaKind()])
			self.quizLabel.set_justify(gtk.JUSTIFY_CENTER)
			self.quizLabel.set_line_wrap(gtk.TRUE)
			box2.pack_start(self.quizLabel)
	
			#The arrow.
			arrow = gtk.Arrow(gtk.ARROW_RIGHT,gtk.SHADOW_IN)
			self.nextButton = gtk.Button()
			self.nextButton.add(arrow)
	
			if self.param.val('answer_mode')=="list":
				#Choice buttons generation.
				self.answerButt = {}; i=0
				for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
					if x[-2:]=="-2": x = x[:-2]
					self.answerButt[i] = gtk.Button(x.upper())
					self.answerButt[i].connect("clicked",self.checkAnswer)
					box2.pack_start(self.answerButt[i])
					i+=1
				self.handlerid = self.nextButton.connect("clicked",self.newQuestion)
			else: 
				self.answerButt = gtk.Entry(3)
				self.answerButt.connect("changed",lambda widget: widget.set_text(widget.get_text().upper()))
				self.answerButt.set_width_chars(3)
				box2.pack_start(self.answerButt)
				self.handlerid = self.nextButton.connect("clicked",self.checkAnswer)
	
			box2.pack_start(self.nextButton)
			box.pack_end(box2)
	
			#Forget the old box
			self.window.remove(oldbox)
			#Then add the new one
			self.window.add(box)
			self.window.show_all()
	
			if self.param.val('answer_mode')=="list": self.nextButton.hide() #Hide the arrow.

		else:	
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING,gtk.BUTTONS_OK,str(48))
			dialog.set_title(str(47))
			dialog.connect('response', lambda dialog, response: dialog.destroy())
			dialog.show()

	def checkAnswer(self,widget):
		"""Check the given answer, update the score
		and display the result."""

		if self.kana[-2:]=="-2": self.kana = self.kana[:-2]

		if self.param.val('answer_mode')=="list": answer = widget.get_label().lower()
		else: answer = self.answerButt.get_text().lower()

		if answer==self.kana: 
			self.quizLabel.set_text("<span color='darkgreen'><b>%s</b></span>" % str(7))
			self.score.update(1) #Update the score (add 1 point).
		else:
			self.quizLabel.set_text("<span color='red'><b>%s</b></span>\n%s" % (str(8),str(9) % "<b>%s</b>" % self.kana.upper()))
			self.score.update() #Update the score.
		self.quizLabel.set_use_markup(gtk.TRUE)

		if self.param.val('answer_mode')=="list":
			for butt in self.answerButt.values(): butt.hide() #Hide choices buttons.
			self.nextButton.show() #Show the arrow.
		else:
			self.answerButt.hide()
			self.nextButton.disconnect(self.handlerid)
			self.handlerid = self.nextButton.connect("clicked",self.newQuestion)

		if self.score.isQuizFinished(self.param.val('length')):
			#The quiz is finished... Let's show results!
			self.nextButton.disconnect(self.handlerid)
			self.handlerid = self.nextButton.connect("clicked",self.results)

	def newQuestion(self,widget):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana(
			self.param.val('basic_katakana'),
			self.param.val('modified_katakana'),
			self.param.val('contracted_katakana'),
			self.param.val('additional_katakana'),
			self.param.val('basic_hiragana'),
			self.param.val('modified_hiragana'),
			self.param.val('contracted_hiragana'))

		self.kanaImage.set_from_file("data/img/kana/%s_%s.gif" % (("k","h")[self.kanaEngine.getKanaKind()],self.kana)) #Update kana's image

		self.quizLabel.set_text((str(5),str(6))[self.kanaEngine.getKanaKind()])

		if self.param.val('answer_mode')=="list":
			self.nextButton.hide() #Hide the arrow.
			#Display the random list.
			i=0
			for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
				if x[-2:]=="-2": x = x[:-2]
				self.answerButt[i].set_label(x.upper())
				self.answerButt[i].show()
				i+=1
		else:  #Display the text entry.
			self.answerButt.set_text("")
			self.answerButt.show()
			self.nextButton.disconnect(self.handlerid)
			self.handlerid = self.nextButton.connect("clicked",self.checkAnswer)
	
	def results(self,data):
		#Display results.
		self.quizLabel.set_text("<big>%s</big>\n\n%s\n%s\n%s" % (str(10),str(11) % self.score.getResults()[0],str(12) % self.score.getResults()[1],str(13) % self.score.getResults()[2]))
		self.quizLabel.set_use_markup(gtk.TRUE)

		self.score.reset() #Reset the score.
		self.kanaImage.hide() #Hide kana image.

		#Connect the arrow to the "main".
		self.nextButton.disconnect(self.handlerid)
		self.nextButton.connect_object("clicked",self.main,self.window.get_child())

	def options(self,oldbox):
		#Dicts for integrer to string options convertion and vice-versa...
		opt_boolean = {0:'false',1:'true','false':0,'true':1}
		opt_answer_mode = {0:'list',1:'entry','list':0,'entry':1}
		opt_list_size = {0:'2',1:'3',2:'4','2':0,'3':1,'4':2}
		opt_length = {0:'short',1:'normal',2:'long','short':0,'normal':1,'long':2}
		opt_lang = {0:'en',1:'fr',2: 'pt_BR',3:'sv','en':0,'fr':1,'pt_BR':2,'sv':3}

		def callback(widget,special=None):
			if special=="save":
				#Update the configuration.
				self.param.write({
				'basic_hiragana':opt_boolean[option1.get_active()],
				'modified_hiragana':opt_boolean[option2.get_active()],
				'contracted_hiragana':opt_boolean[option3.get_active()],
				'basic_katakana':opt_boolean[option4.get_active()],
				'modified_katakana':opt_boolean[option5.get_active()],
				'contracted_katakana':opt_boolean[option6.get_active()],
				'additional_katakana':opt_boolean[option7.get_active()],
				'answer_mode':opt_answer_mode[option8.get_history()],
				'list_size':opt_list_size[option9.get_history()],
				'length':opt_length[option10.get_history()],
				'lang':opt_lang[option11.get_history()]
				})
			self.main(box) #Go back to the "main".

		def parts_popup(widget,kanaset):
			label = gtk.Label(str(22))	

		self.window.set_title(str(2)) #Change title of window.
		box = gtk.VBox(spacing=3)

		label = gtk.Label(str(14))
		box.pack_start(label,gtk.FALSE)
		box2 = gtk.HBox()
		box.pack_start(box2)
		box3 = gtk.VBox()
		box2.pack_start(box3)

		frame = gtk.Frame(str(15))
		box3.pack_start(frame)
		table = gtk.Table(3,3)
		table.set_row_spacings(2)
		table.set_border_width(2)
		frame.add(table)

		#`basic_hiragana'
		image = gtk.Image()
		image.set_from_file("data/img/basic_hiragana.gif")
		table.attach(image,0,1,0,1)
		option1 = gtk.CheckButton(str(17))
		option1.set_active(opt_boolean[self.param.val('basic_hiragana')])
		table.attach(option1,1,2,0,1)
		button = gtk.Button(str(21))
		button.set_sensitive(option1.get_active())
		option1.connect("toggled",lambda *args: args[1].set_sensitive(option1.get_active()),button)
		table.attach(button,2,3,0,1)
		
		#`modified_hiragana'
		image = gtk.Image()
		image.set_from_file("data/img/modified_hiragana.gif")
		table.attach(image,0,1,1,2)
		option2 = gtk.CheckButton(str(18))
		option2.set_active(opt_boolean[self.param.val('modified_hiragana')])
		table.attach(option2,1,2,1,2)
		button = gtk.Button(str(21))
		button.set_sensitive(option2.get_active())
		option2.connect("toggled",lambda *args: args[1].set_sensitive(option2.get_active()),button)
		table.attach(button,2,3,1,2)

		#`contracted_hiragana'
		image = gtk.Image()
		image.set_from_file("data/img/contracted_hiragana.gif")
		table.attach(image,0,1,2,3)
		option3 = gtk.CheckButton(str(19))
		option3.set_active(opt_boolean[self.param.val('contracted_hiragana')])
		table.attach(option3,1,2,2,3)
		button = gtk.Button(str(21))
		button.set_sensitive(option3.get_active())
		option3.connect("toggled",lambda *args: args[1].set_sensitive(option3.get_active()),button)
		table.attach(button,2,3,2,3)

		frame = gtk.Frame(str(16))
		box3.pack_start(frame)
		table = gtk.Table(3,4)
		table.set_row_spacings(2)
		table.set_border_width(2)
		frame.add(table)

		#`basic_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/basic_katakana.gif")
		table.attach(image,0,1,0,1)
		option4 = gtk.CheckButton(str(17))
		option4.set_active(opt_boolean[self.param.val('basic_katakana')])
		table.attach(option4,1,2,0,1)
		button = gtk.Button(str(21))
		button.set_sensitive(option4.get_active())
		option4.connect("toggled",lambda *args: args[1].set_sensitive(option4.get_active()),button)
		table.attach(button,2,3,0,1)
		
		#`modified_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/modified_katakana.gif")
		table.attach(image,0,1,1,2)
		option5 = gtk.CheckButton(str(18))
		option5.set_active(opt_boolean[self.param.val('modified_katakana')])
		table.attach(option5,1,2,1,2)
		button = gtk.Button(str(21))
		button.set_sensitive(option5.get_active())
		option5.connect("toggled",lambda *args: args[1].set_sensitive(option5.get_active()),button)
		table.attach(button,2,3,1,2)

		#`contracted_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/contracted_katakana.gif")
		table.attach(image,0,1,2,3)
		option6 = gtk.CheckButton(str(19))
		option6.set_active(opt_boolean[self.param.val('contracted_katakana')])
		table.attach(option6,1,2,2,3)
		button = gtk.Button(str(21))
		button.set_sensitive(option6.get_active())
		option6.connect("toggled",lambda *args: args[1].set_sensitive(option6.get_active()),button)
		table.attach(button,2,3,2,3)

		#`additional_katakana'
		image = gtk.Image()
		image.set_from_file("data/img/additional_katakana.gif")
		table.attach(image,0,1,3,4)
		option7 = gtk.CheckButton(str(20))
		option7.set_active(opt_boolean[self.param.val('additional_katakana')])
		table.attach(option7,1,2,3,4)
		button = gtk.Button(str(21))
		button.set_sensitive(option7.get_active())
		option7.connect("toggled",lambda *args: args[1].set_sensitive(option7.get_active()),button)
		table.attach(button,2,3,3,4)

		table = gtk.Table(1,8)
		table.set_border_width(6)
		box2.pack_start(table)

		#`answer_mode'
		label = gtk.Label(str(23))
		table.attach(label,0,1,0,1)
		menu = gtk.Menu()
		for val in (str(24),str(25)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option8 = gtk.OptionMenu()
		option8.set_menu(menu)
		option8.set_history(opt_answer_mode[self.param.val('answer_mode')])
		table.attach(option8,0,1,1,2)

		#`list_size'
		label = gtk.Label(str(26))
		table.attach(label,0,1,2,3)
		menu = gtk.Menu()
		for val in (str(27),str(28),str(29)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option9 = gtk.OptionMenu()
		option9.set_menu(menu)
		option9.set_history(opt_list_size[self.param.val('list_size')])
		table.attach(option9,0,1,3,4)

		#`length'
		label = gtk.Label(str(30))
		table.attach(label,0,1,4,5)
		menu = gtk.Menu()
		for val in (str(31),str(32),str(33)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option10 = gtk.OptionMenu()
		option10.set_menu(menu)
		option10.set_history(opt_length[self.param.val('length')])
		table.attach(option10,0,1,5,6)

		#`lang'
		label = gtk.Label(str(34))
		table.attach(label,0,1,6,7)
		menu = gtk.Menu()
		for val in (str(35),str(36),str(37),str(38)):
			item = gtk.MenuItem(val)
			menu.append(item)
		option11 = gtk.OptionMenu()
		option11.set_menu(menu)
		option11.set_history(opt_lang[self.param.val('lang')])
		table.attach(option11,0,1,7,8)

		#Buttons at bottom...
		box2 = gtk.HBox()
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

			dialog = gtk.Dialog(str(4),flags=gtk.DIALOG_NO_SEPARATOR)
			dialog.connect("destroy",self.destroy,"about")

			#Border and spacing...
			dialog.set_border_width(5)
			dialog.vbox.set_spacing(5)

			label = gtk.Label("<span color='#008'><b>%s</b>\n%s\nCopyleft 2003, 2004 Choplair-network.</span>" % (str(41),str(42) % self.version))
			label.set_justify(gtk.JUSTIFY_CENTER)
			label.set_use_markup(gtk.TRUE)
			dialog.vbox.pack_start(label)

			label = gtk.Label(str(43))
			label.set_line_wrap(gtk.TRUE)
			dialog.vbox.pack_start(label)

			frame = gtk.Frame(str(44))
			box = gtk.HBox()

			logo = gtk.Image()
			logo.set_from_file("data/img/chprod.png")
			box.pack_start(logo,gtk.FALSE)

			label = gtk.Label("%s\n\nhttp://www.choplair.org/" % str(45))
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

