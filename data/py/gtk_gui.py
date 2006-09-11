"""Kana no quiz!
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
# Imports.
import gtk
import os.path
from pango import FontDescription
from string import capwords
# Internal modules.
import kanaengine
import score
import i18n

class Gui:
	def __init__(self, *args):
		self.param = args[0]
		self.version = args[1]
		self.datarootpath = args[2]

		self.window = gtk.Window()
		self.kanaEngine =  kanaengine.KanaEngine()
		self.score = score.Score()

		#Localization.
		self.i18n = i18n.I18n(os.path.join(self.datarootpath, "locale"))
		self.currentlang = self.param.val('lang')
		self.i18n.setlang(self.param.val('lang'))

		global msg
		msg = self.i18n.msg

		#Initial window attributes.
		self.window.set_title(msg(0))
		self.window.connect("destroy",self.quit)
		self.window.set_border_width(5)
		gtk.window_set_default_icon_from_file(os.path.join(
			self.datarootpath,"img","icon.png"))
		self.handlerid = {}

	def main(self,oldbox=None):
		if self.currentlang!=self.param.val('lang'):
			#Change localization...
			self.currentlang = self.param.val('lang')
			self.i18n.setlang(self.param.val('lang'))
			global str
			str = self.i18n.str

		if oldbox: 
			self.window.set_title(msg(0))
			self.window.resize(1,1) #Properly resize the window.

		box = gtk.HBox()

		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img","logo.gif"))
		box.pack_start(image,False)

		box2 = gtk.VBox()
		button = gtk.Button(msg(1))
		button.connect_object("clicked",self.intro,box)
		box2.pack_start(button)
		button = gtk.Button(msg(2))
		button.connect_object("clicked",self.options,box)
		box2.pack_start(button)
		button = gtk.Button(msg(3))
		button.connect_object("clicked",self.quiz,box)
		box2.pack_start(button)
		button = gtk.Button(msg(4))
		button.connect("clicked",self.about)
		box2.pack_start(button)
		button = gtk.Button(msg(71))
		button.connect("clicked",self.quit)
		box2.pack_start(button)
		box.pack_start(box2)

		if oldbox: self.window.remove(oldbox)
		self.window.add(box)
		self.window.show_all()

		#Initialize pyGTK if it haven't been done yet.
		if not oldbox : gtk.main()

	def intro(self, oldbox):
		#Here comes the marvelous introduction...
		self.window.set_title(msg(1)) #Change title of window.
		box = gtk.VBox(spacing=5)

		label = gtk.Label(msg(5))
		label.set_line_wrap(True)
		box.pack_start(label)

		label = gtk.Label(msg(6))
		label.set_line_wrap(True)
		box.pack_start(label)

		label = gtk.Label(msg(7))
		label.set_line_wrap(True)
		box.pack_start(label)

		label = gtk.Label(msg(8))
		label.set_line_wrap(True)
		box.pack_start(label)

		label = gtk.Label(msg(9))
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
			box = gtk.HBox(spacing=4)
			box2 = gtk.VBox()
			#Kana image.
			self.kanaImage = gtk.Image()
			#Initialy setting kana's image.
			self.setKanaImage(self.kanaEngine.getKanaKind(),self.kana) 
			box2.pack_start(self.kanaImage,False)
			#Quiz informations.
			self.quizInfos = {}
			self.quizInfos['questionNumLabel'] = gtk.Label(msg(67) % (
				self.score.getQuestionTotal()+1,self.param.val('length')))
			self.quizInfos['systemLabel'] = gtk.Label(msg(68) % capwords(
				self.param.val('transcription_system')))
			box3 = gtk.VBox(spacing=2)
			box3.pack_start(self.quizInfos['questionNumLabel'])
			box3.pack_start(self.quizInfos['systemLabel'])
			box2.pack_start(box3)
			self.quizInfos['container'] = gtk.EventBox()
			self.quizInfos['container'].modify_bg(gtk.STATE_NORMAL,
				gtk.gdk.color_parse("white"))
			self.quizInfos['container'].add(box2)
			box.pack_start(self.quizInfos['container'],False)

			box2 = gtk.VBox(spacing=4)
			#Stop button.
			self.quizWidget['stop'] = gtk.Button(stock=gtk.STOCK_STOP)
			self.quizWidget['stop'].connect("clicked",self.results)
			box2.pack_start(self.quizWidget['stop'],False)
			#Question label.
			self.quizLabel = gtk.Label((msg(11),msg(12))[self.kanaEngine.getKanaKind()])
			self.quizLabel.set_justify(gtk.JUSTIFY_CENTER)
			self.quizLabel.set_line_wrap(True)
			box2.pack_start(self.quizLabel)

			#Arrow.
			arrow = gtk.Arrow(gtk.ARROW_RIGHT,gtk.SHADOW_IN)
			self.nextButton = gtk.Button()
			self.nextButton.add(arrow)

			if self.param.val('answer_mode')=="list":
				#Choice buttons generation.
				self.answerButt = {}; i=0

				for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
					#If the selected romanization system is *other* than Hepburn (default),
					#let's convert that answer list (given in the Hepburn internal format)
					#into the user-selected romanization system.
					if self.param.val('transcription_system')!="hepburn":
						x = kanaengine.HepburnToOtherSysConvert(x,
							self.param.val('transcription_system'))
					if x[-2:]=="-2": x = x[:-2]
					self.answerButt[i] = gtk.Button(x.upper())
					self.answerButt[i].connect("clicked",self.checkAnswer)
					box2.pack_start(self.answerButt[i])
					i+=1
				self.handlerid['nextbutton_clicked'] = self.nextButton.connect("clicked",
					self.newQuestion)
			else: 
				entry = gtk.Entry(3)
				entry.modify_font(FontDescription("normal 35"))
				entry.set_alignment(0.5)
				entry.set_width_chars(3)
				entry.connect("changed",lambda widget: widget.set_text(
					widget.get_text().upper()))
				box2.pack_start(entry)
				self.handlerid['nextbutton_clicked'] = self.nextButton.connect_object(
					"clicked",self.checkAnswer,entry)
				entry.connect("activate",lambda widget: self.nextButton.clicked())

			box2.pack_start(self.nextButton)
			box.pack_end(box2)

			#Forgetting the old box.
			self.window.remove(oldbox)
			#Then addding the new one.
			self.window.add(box)

			self.window.show_all()

			#Hide the arrow.
			if self.param.val('answer_mode')=="list": self.nextButton.hide() 
			else: entry.grab_focus() #Giving focus to text entry.

			self.quizWidget['stop'].hide() #Hiding the stop button.

		else:
			dialog = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL,
				gtk.MESSAGE_WARNING,gtk.BUTTONS_OK,msg(60))
			dialog.connect('response', lambda dialog, response: dialog.destroy())
			dialog.show()

	def checkAnswer(self,widget):
		"""Check the given answer, update the score
			and display the result.
			
		"""

		if self.param.val('answer_mode')=="list":
			answer = widget.get_label().lower()
		else: answer = widget.get_text().lower()
		#If the selected romanization system is *other* than Hepburn (default),
		#let's convert the good answer (given in the Hepburn internal format)
		#to the user-selected romanization system, in order to compare with its
		#chosen answer.
		if self.param.val('transcription_system')!="hepburn":
			self.kana = kanaengine.HepburnToOtherSysConvert(self.kana,
				self.param.val('transcription_system')).lower()
		if self.kana[-2:]=="-2": self.kana = self.kana[:-2]

		if answer==self.kana: # \o/
			self.quizLabel.set_text("<span color='darkgreen'><b>%s</b></span>" %
				msg(13))
			self.score.update(1) #Update the score (add 1 point).
		else: # /o\
			self.quizLabel.set_text("<span color='red'><b>%s</b></span>\n%s" %
				(msg(14),msg(15) % "<big><b>%s</b></big>" % self.kana.upper()))
			#Updating the score (indicating unrecognized kana).
			self.score.update(0,self.kana,self.kanaEngine.getKanaKind()) 
		self.quizLabel.set_use_markup(True)

		if self.param.val('answer_mode')=="list":
			for butt in self.answerButt.values():
				butt.hide() #Hide choices buttons.
			self.nextButton.show() #Show the arrow.
		else:
			widget.hide()
			self.nextButton.disconnect(self.handlerid['nextbutton_clicked'])
			self.handlerid['nextbutton_clicked'] = self.nextButton.connect_object(
				"clicked",self.newQuestion,widget)

		self.nextButton.grab_focus() #Give focus to the arrow.

		if self.score.isQuizFinished(self.param.val('length')):
			#The quiz is finished... Let's show results!
			self.nextButton.disconnect(self.handlerid['nextbutton_clicked'])
			self.handlerid['nextbutton_clicked'] = self.nextButton.connect("clicked",
				self.results)
		else: self.quizWidget['stop'].show()

	def newQuestion(self,widget):
		#Randomly get a kana.
		self.kana = self.kanaEngine.randomKana()

		#Update kana's image.
		self.setKanaImage(self.kanaEngine.getKanaKind(),self.kana) 

		self.quizInfos['questionNumLabel'].set_text(msg(67) %
			(self.score.getQuestionTotal()+1,self.param.val('length')))
		self.quizLabel.set_text((msg(11),msg(12))[self.kanaEngine.getKanaKind()])

		if self.param.val('answer_mode')=="list":
			self.nextButton.hide() #Hide the arrow.
			#Display the random list.
			i=0
			for x in self.kanaEngine.randomAnswers(self.param.val('list_size')):
				#If the selected romanization system is *other* than Hepburn (default),
				#let's convert that answer list (given in the Hepburn internal format)
				#into the user-selected romanization system.
				if self.param.val('transcription_system')!="hepburn":
					x = kanaengine.HepburnToOtherSysConvert(x,self.param.val(
						'transcription_system'))
				if x[-2:]=="-2": x = x[:-2]
				self.answerButt[i].set_label(x.upper())
				self.answerButt[i].show()
				i+=1

		else:  #Display the text entry.
			widget.set_text("")
			widget.show()
			widget.grab_focus() #Give focus to text entry.
			self.nextButton.disconnect(self.handlerid['nextbutton_clicked'])
			self.handlerid['nextbutton_clicked'] = self.nextButton.connect_object(
				"clicked",self.checkAnswer,widget)

		self.quizWidget['stop'].hide() #Hide the stop button.

	def results(self,data):
		results = self.score.getResults()
		#Displaying results.
		text = "<big>%s</big>\n\n%s\n%s\n%s" % (msg(16),msg(17) % results[0],
			msg(18) % results[1],msg(19) % results[2])

		def getUnrecmsg(kind):
			"""Return a ready-to-display string which indicates the
				unrecognized kana (by kind) during the quiz.
			
			"""
			plop = ""
			for key,val in results[3][kind].items():
				for x in val: 
					if key!=1: plop += "%s (%s), " % (x.upper(),key)
					else: plop += "%s, " % x.upper()
			return "\n%s" % msg(72+kind) % plop[:-2]

		if len(results[3][0])>0: text += getUnrecmsg(0)
		if len(results[3][1])>0: text += getUnrecmsg(1)

		self.quizLabel.set_text(text)
		self.quizLabel.set_use_markup(True)

		self.score.reset() #Reseting the score.
		self.kanaEngine.reset() #Reseting kana engine's variables.
		self.kanaImage.hide() #Hidding kana image.
		self.quizInfos['container'].hide() #Hidding quiz stop & informations.

		#Connecting the arrow to the ``main".
		self.nextButton.disconnect(self.handlerid['nextbutton_clicked'])
		self.nextButton.connect_object("clicked",self.main,self.window.get_child())
		self.quizWidget['stop'].hide() #Hidding the stop button.

	def options(self,oldbox):
		#Dicts for integrer to string param convertion and vice-versa...
		opt_conv = {
			"boolean":{0:'false',1:'true','false':0,'true':1},
			"transcription_system":{0:'hepburn',1:'kunrei-shiki',2:'nihon-shiki',
				3:'polivanov','hepburn':0,'kunrei-shiki':1,'nihon-shiki':2,'polivanov':3},
			"answer_mode":{0:'list',1:'entry','list':0,'entry':1},
			"rand_answer_sel_range":{0:'portion',1:'set',2:'kind','portion':0,
				'set':1,'kind':2},
			"lang":{0:'en',1:'fr',2:'de',3:'pt_BR',4:'ru',5:'sr',6:'sv','en':0,'fr':1,
				'de':2,'pt_BR':3,'ru':4,'sr':5,'sv':6}
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

		def callback(widget,special=None):
			if special=="save":
				#Update the configuration.
				self.param.write({
				'basic_hiragana':opt_conv["boolean"][option1.get_active()],
				'basic_hiragana_portions':kanaPortions[0],
				'modified_hiragana':opt_conv["boolean"][option2.get_active()],
				'modified_hiragana_portions':kanaPortions[1],
				'contracted_hiragana':opt_conv["boolean"][option3.get_active()],
				'contracted_hiragana_portions':kanaPortions[2],
				'basic_katakana':opt_conv["boolean"][option4.get_active()],
				'basic_katakana_portions':kanaPortions[3],
				'modified_katakana':opt_conv["boolean"][option5.get_active()],
				'modified_katakana_portions':kanaPortions[4],
				'contracted_katakana':opt_conv["boolean"][option6.get_active()],
				'contracted_katakana_portions':kanaPortions[5],
				'additional_katakana':opt_conv["boolean"][option7.get_active()],
				'additional_katakana_portions':kanaPortions[6],
				'transcription_system':opt_conv["transcription_system"][
					option8.get_active()],
				'answer_mode':opt_conv["answer_mode"][option9.get_active()],
				'list_size':option10.get_active()+2,
				'rand_answer_sel_range':opt_conv["rand_answer_sel_range"][
					option11.get_active()],
				'length':int(option12.get_value()),
				'kana_no_repeat':opt_conv["boolean"][option13.get_active()],
				'lang':opt_conv["lang"][option14.get_active()]
				})
			self.main(box) #Go back to the ``main".

		def portions_popup(widget,kanaset):
			temp_list = list(kanaPortions[kanaset]) #Temporary portion list.

			#Callbacks.
			def newValue(widget,num):
				#Update the emporary variable value.
				temp_list[num] = (0,1)[widget.get_active()] 
			def selectAll(widget): 
				for x in widget.get_children(): x.set_active(True)
			def validedChanges(*args):
				"""Check for a least one selected kana portion (display of a message
					if not the case), catch parameters, then close the window.

				"""
				if not 1 in temp_list:
					dialog2 = gtk.MessageDialog(self.window,gtk.DIALOG_MODAL,
						gtk.MESSAGE_INFO,gtk.BUTTONS_OK,msg(66))
					dialog2.connect('response', lambda dialog, response: dialog.destroy())
					dialog2.show()

					if kanaset==0: widget = option1
					elif kanaset==1: widget = option2
					elif kanaset==2: widget = option3
					elif kanaset==3: widget = option4
					elif kanaset==4: widget = option5
					elif kanaset==5: widget = option6
					elif kanaset==6: widget = option7
					widget.set_active(False)

				kanaPortions[kanaset] = temp_list
				dialog.destroy()

			dialog = gtk.Dialog(msg(28+kanaset),self.window,gtk.DIALOG_MODAL)
			dialog.vbox.set_spacing(3)

			label = gtk.Label(msg(35))
			label.set_line_wrap(True)
			dialog.vbox.pack_start(label)

			set = self.kanaEngine.getASet(kanaset)

			label = gtk.Label(msg(36))
			label.set_line_wrap(True)
			dialog.vbox.pack_start(label)
			table = gtk.Table(2,abs(len(set)/2+1))
			dialog.vbox.pack_start(table)

			j,k = 1,0
			for i in range(len(set)):
				string = ""
				for kana in set[i]: string += "%s " % kana.upper()
				check = gtk.CheckButton(string[:-1])
				check.connect("toggled",newValue,i)
				if temp_list[i]==1: check.set_active(True)
				if j: table.attach(check,0,1,k,k+1); j=0
				else: table.attach(check,1,2,k,k+1); j=1; k+=1

			button = gtk.Button(msg(37))
			button.connect_object("clicked",selectAll,table)
			#If nothing selected, select all. :p
			if not 1 in kanaPortions[kanaset]: button.emit("clicked")
			dialog.vbox.pack_start(button)

			#Buttons at bottom...
			button = gtk.Button(stock=gtk.STOCK_OK)
			button.connect("clicked",validedChanges)
			dialog.action_area.pack_end(button)
			button = gtk.Button(stock=gtk.STOCK_CANCEL)
			button.connect("clicked",lambda *args: dialog.destroy())
			dialog.action_area.pack_end(button)

			dialog.show_all()

		self.window.set_title(msg(2)) #Change title of window.
		da_box = gtk.HBox(spacing=3)
		toolbar = gtk.Toolbar()
		toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
		toolbar.set_style(gtk.TOOLBAR_BOTH)
		toolbar.insert_item(msg(83), None, None, None, None, None, -1)
		toolbar.insert_item(msg(84), None, None, None, None, None, -1)
		toolbar.insert_item(msg(85), None, None, None, None, None, -1)
		toolbar.insert_item(msg(86), None, None, None, None, None, -1)
		da_box.pack_start(toolbar)
		box = gtk.VBox(spacing=3)
		da_box.pack_start(box)

		label = gtk.Label(msg(20))
		box.pack_start(label,False)
		box2 = gtk.HBox()
		box.pack_start(box2)
		box3 = gtk.VBox()
		box2.pack_start(box3)

		frame = gtk.Frame(msg(21))
		box3.pack_start(frame)
		table = gtk.Table(3,3)
		table.set_row_spacings(2)
		table.set_col_spacing(0,2)
		table.set_border_width(2)
		frame.add(table)

		#`basic_hiragana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"basic_hiragana.gif"))
		table.attach(image,0,1,0,1)
		option1 = gtk.CheckButton(msg(23))
		option1.set_active(opt_conv["boolean"][self.param.val('basic_hiragana')])
		table.attach(option1,1,2,0,1)
		button = gtk.Button(msg(27))
		button.connect("clicked",portions_popup,0)
		button.set_sensitive(option1.get_active())
		option1.connect("toggled",lambda *args: args[1].set_sensitive(
			option1.get_active()),button)
		table.attach(button,2,3,0,1)

		#`modified_hiragana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"modified_hiragana.gif"))
		table.attach(image,0,1,1,2)
		option2 = gtk.CheckButton(msg(24))
		option2.set_active(opt_conv["boolean"][self.param.val('modified_hiragana')])
		table.attach(option2,1,2,1,2)
		button = gtk.Button(msg(27))

		button.connect("clicked",portions_popup,1)
		button.set_sensitive(option2.get_active())
		option2.connect("toggled",lambda *args: args[1].set_sensitive(
			option2.get_active()),button)
		table.attach(button,2,3,1,2)

		#`contracted_hiragana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"contracted_hiragana.gif"))
		table.attach(image,0,1,2,3)
		option3 = gtk.CheckButton(msg(25))
		option3.set_active(opt_conv["boolean"][self.param.val(
			'contracted_hiragana')])
		table.attach(option3,1,2,2,3)
		button = gtk.Button(msg(27))
		button.connect("clicked",portions_popup,2)
		button.set_sensitive(option3.get_active())
		option3.connect("toggled",lambda *args: args[1].set_sensitive(
			option3.get_active()),button)
		table.attach(button,2,3,2,3)

		frame = gtk.Frame(msg(22))
		box3.pack_start(frame)
		table = gtk.Table(3,4)
		table.set_row_spacings(2)
		table.set_col_spacing(0,2)
		table.set_border_width(2)
		frame.add(table)

		#`basic_katakana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"basic_katakana.gif"))
		table.attach(image,0,1,0,1)
		option4 = gtk.CheckButton(msg(23))
		option4.set_active(opt_conv["boolean"][self.param.val('basic_katakana')])
		table.attach(option4,1,2,0,1)
		button = gtk.Button(msg(27))
		button.connect("clicked",portions_popup,3)
		button.set_sensitive(option4.get_active())
		option4.connect("toggled",lambda *args: args[1].set_sensitive(
			option4.get_active()),button)
		table.attach(button,2,3,0,1)

		#`modified_katakana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"modified_katakana.gif"))
		table.attach(image,0,1,1,2)
		option5 = gtk.CheckButton(msg(24))
		option5.set_active(opt_conv["boolean"][self.param.val('modified_katakana')])
		table.attach(option5,1,2,1,2)
		button = gtk.Button(msg(27))
		button.connect("clicked",portions_popup,4)
		button.set_sensitive(option5.get_active())
		option5.connect("toggled",lambda *args: args[1].set_sensitive(
			option5.get_active()),button)
		table.attach(button,2,3,1,2)

		#`contracted_katakana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"contracted_katakana.gif"))
		table.attach(image,0,1,2,3)
		option6 = gtk.CheckButton(msg(25))
		option6.set_active(opt_conv["boolean"][self.param.val('contracted_katakana')])
		table.attach(option6,1,2,2,3)
		button = gtk.Button(msg(27))
		button.connect("clicked",portions_popup,5)
		button.set_sensitive(option6.get_active())
		option6.connect("toggled",lambda *args: args[1].set_sensitive(
			option6.get_active()),button)
		table.attach(button,2,3,2,3)

		#`additional_katakana'
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img",
			"additional_katakana.gif"))
		table.attach(image,0,1,3,4)
		option7 = gtk.CheckButton(msg(26))
		option7.set_active(opt_conv["boolean"][self.param.val('additional_katakana')])
		table.attach(option7,1,2,3,4)
		button = gtk.Button(msg(27))
		button.connect("clicked",portions_popup,6)
		button.set_sensitive(option7.get_active())
		option7.connect("toggled",lambda *args: args[1].set_sensitive(
			option7.get_active()),button)
		table.attach(button,2,3,3,4)

		box3 = gtk.VBox(spacing=2)
		box3.set_border_width(6)
		box2.pack_start(box3)

		#`transcription_system'
		label = gtk.Label(msg(61))
		box3.pack_start(label)
		option8 = gtk.combo_box_new_text()
		for val in (msg(62),msg(63),msg(64),msg(79)):
			option8.append_text(val)
		option8.set_active(opt_conv["transcription_system"][self.param.val(
			'transcription_system')])
		box3.pack_start(option8)

		#`answer_mode'
		label = gtk.Label(msg(38))
		box3.pack_start(label)
		option9 = gtk.combo_box_new_text()
		for val in (msg(39),msg(40)):
			option9.append_text(val)
		option9.set_active(opt_conv["answer_mode"][self.param.val('answer_mode')])
		box3.pack_start(option9)

		#`list_size'
		label = gtk.Label(msg(41))
		box3.pack_start(label)
		option10 = gtk.combo_box_new_text()
		for val in (2,3,4,5):
			option10.append_text(msg(42) % val)
		option10.set_active(self.param.val('list_size')-2)
		box3.pack_start(option10)

		#`rand_answer_sel_range'
		label2 = gtk.Label(msg(75))
		box3.pack_start(label2)
		option11 = gtk.combo_box_new_text()
		for val in (msg(76),msg(77),msg(78)):
			option11.append_text(val)
		option11.set_active(opt_conv["rand_answer_sel_range"][self.param.val(
			'rand_answer_sel_range')])
		box3.pack_start(option11)

		#Bouyaka!
		def bouyaka(widget,targets):
			"""Set list size widgets sensitive state according
				to answer mode widget selected param.
			
			"""
			for x in targets: x.set_sensitive(not widget.get_active())
		bouyaka(option9,(label,option10,label2,option11))
		option9.connect("changed",bouyaka,(label,option10,label2,option11))

		#`length'
		box4 = gtk.HBox()
		label = gtk.Label(msg(43))
		box4.pack_start(label)
		adjustment = gtk.Adjustment(float(self.param.val('length')),1,200,1,10)
		option12 = gtk.SpinButton(adjustment)
		option12.set_alignment(0.5)
		box4.pack_start(option12)
		box4.pack_end(gtk.Label(msg(80)),False)
		box3.pack_start(box4)

		#`kana_no_repeat'
		option13 = gtk.CheckButton(msg(44))
		option13.set_active(opt_conv["boolean"][self.param.val('kana_no_repeat')])
		box3.pack_start(option13)

		#`lang'
		label = gtk.Label(msg(45))
		box3.pack_start(label)
		option14 = gtk.combo_box_new_text()
		for val in (msg(46),msg(47),msg(70),msg(48),msg(74),msg(49),msg(50)):
			option14.append_text(val)
		option14.set_active(opt_conv["lang"][self.param.val('lang')])
		box3.pack_start(option14)

		#Buttons at bottom...
		box2 = gtk.HBox()
		button = gtk.Button(stock=gtk.STOCK_SAVE)
		button.connect("clicked",callback,"save")
		box2.pack_start(button)
		button = gtk.Button(stock=gtk.STOCK_CANCEL)
		button.connect("clicked",callback)
		box2.pack_start(button)
		box.pack_end(box2,False)

		#Remove the old box then add the new one.
		self.window.remove(oldbox)
		self.window.add(da_box)

		self.window.show_all()

	def about(self,widget):
		dialog = gtk.Dialog(msg(4),self.window,gtk.DIALOG_NO_SEPARATOR|
			gtk.DIALOG_MODAL,(gtk.STOCK_CLOSE,gtk.RESPONSE_CLOSE))
		dialog.set_border_width(5)
		dialog.vbox.set_spacing(4)

		box = gtk.HBox(spacing=6)
		image = gtk.Image()
		image.set_from_file(os.path.join(self.datarootpath,"img","icon.png"))
		box.pack_start(image)
		box2 = gtk.VBox()
		label = gtk.Label("<span color='#008'><b>%s</b>\n%s (GTK+)</span>" %
			(msg(53),msg(54) % self.version))
		label.set_justify(gtk.JUSTIFY_CENTER)
		label.set_use_markup(True)
		box2.pack_start(label)
		label = gtk.Label("Copyleft 2003, 2004, 2005, 2006 Choplair-network.")
		box2.pack_start(label)
		box.pack_start(box2)
		dialog.vbox.pack_start(box)

		label = gtk.Label(msg(55))
		label.set_line_wrap(True)
		label.set_justify(gtk.JUSTIFY_CENTER)
		dialog.vbox.pack_start(label)

		frame = gtk.Frame(msg(56))
		container = gtk.EventBox()
		container.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse("#c9ddff"))
		box = gtk.HBox(spacing=6)
		box.set_border_width(3)

		box2 = gtk.VBox()
		logo = gtk.Image()
		logo.set_from_file(os.path.join(self.datarootpath,"img","chprod.png"))
		box2.pack_start(logo)
		label = gtk.Label("<i>http://www.choplair.org/</i>")
		label.set_selectable(True)
		label.set_use_markup(True)
		box2.pack_start(label)
		box.pack_start(box2,padding=10)

		buffer = gtk.TextBuffer()
		buffer.set_text("%s\n\n%s\n%s" % (msg(57),msg(81),msg(82)))
		buffer.apply_tag(buffer.create_tag(justification=gtk.JUSTIFY_CENTER,
			editable=False),buffer.get_start_iter(),buffer.get_end_iter())
		buffer.apply_tag(buffer.create_tag(weight=700),buffer.get_iter_at_line(4),
			buffer.get_iter_at_line(5))
		textview = gtk.TextView(buffer)
		textview.modify_base(gtk.STATE_NORMAL,gtk.gdk.color_parse("#c9ddff"))
		box.pack_start(textview)

		container.add(box)
		frame.add(container)

		dialog.vbox.pack_start(frame)
		dialog.connect('response', lambda dialog, response: dialog.destroy())
		dialog.show_all()

	def setKanaImage(self,kind,kana):
		"""Updating kana image."""
		self.kanaImage.set_from_file(os.path.join(self.datarootpath,"img","kana",
			"%s_%s.gif" % (("k","h")[kind],kana)))

	def quit(self,widget):
		gtk.main_quit() #Bye~~
