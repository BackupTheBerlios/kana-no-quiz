"""Kana no quiz!

   Copyleft 2003, 2004, 2005, 2006, 2007, 2008, 2009, Choplair-network.
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
import sys
import gtk
import time
import threading
import os.path
from pango import FontDescription
from string import capwords
# Internal modules.
import i18n
import kanaengine
import playsound
import score

class Gui:
   def __init__(self, *args):
      self.param = args[0]
      self.version = args[1]
      self.datarootpath = args[2]

      self.kana_engine =  kanaengine.KanaEngine(self.param)
      self.playsound = playsound.PlaySound(self.datarootpath)
      self.score = score.Score()
      self.handlerid = {}
      self.widgets = {}

      # Localization.
      self.i18n = i18n.I18n(os.path.join(self.datarootpath, "locale"))
      self.currentlang = self.param['lang']
      self.i18n.setlang(self.param['lang'])
      global msg
      msg = self.i18n.msg

      # Initial window attributes.
      self.window = gtk.Window()
      self.window.connect('key-press-event', self.keypress)
      self.window.set_resizable(False)
      self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
      self.window.connect("destroy", self.quit)
      gtk.window_set_default_icon_from_file(os.path.join(
         self.datarootpath, "img", "icon.png"))
      self.win_container = gtk.EventBox()
      self.win_container.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(
         "#f3eddd"))
      self.window.add(self.win_container)

   def keypress(self, source, event):
      widgetNumber = event.keyval - 49
      if ((widgetNumber >= 0 and widgetNumber <= self.param['list_size']) and
         self.__dict__.has_key('answerButt') and
         self.wigets['random_ans_butt'][widgetNumber]):
         self.check_answer(self.wigets['random_ans_butt'][event.keyval - 49])

   def main(self, oldbox=None):
		# This was source of problem.
      #~ if self.currentlang != self.param['lang']:
         #~ # Changing localization...
         #~ self.currentlang = self.param['lang']
         #~ self.i18n.setlang(self.param['lang'])
         #~ global msg
         #~ del msg
         #~ msg = self.i18n.msg

      self.window.set_title(msg(0))
      box = gtk.VBox()
      box.set_border_width(5)

      image = gtk.Image()
      image.set_from_file(os.path.join(self.datarootpath, "img",
         "main_image.png"))
      box.pack_start(image,False)

      box.pack_start(gtk.Label(msg(88) % self.version), False, padding=4)

      table = gtk.Table(2, 3, True)
      button = gtk.Button(msg(1))
      button.connect_object("clicked", self.intro, box)
      table.attach(button, 0, 1, 0, 1)
      button = gtk.Button(msg(87))
      button.connect_object("clicked", self.kana_tables, box)
      table.attach(button, 0, 1, 1, 2)
      button = gtk.Button(msg(2))
      button.connect_object("clicked", self.options, box)
      table.attach(button, 1, 2, 0, 1)
      button = gtk.Button(msg(3))
      button.connect_object("clicked", self.quiz, box)
      table.attach(button, 1, 2, 1, 2)
      button = gtk.Button(msg(4))
      button.connect_object("clicked", self.about, box)
      table.attach(button, 2, 3, 0, 1)
      button = gtk.Button(msg(71))
      button.connect("clicked", self.quit)
      table.attach(button, 2, 3, 1, 2)
      box.pack_start(table)

      if oldbox:
         self.win_container.remove(oldbox)
      self.win_container.add(box)
      self.window.show_all()

      if not oldbox:
         # Initializing pyGTK if it haven't been done yet.
         #gtk.gdk.threads_init()
         gtk.main()

   def intro(self, oldbox):
      """Render the marvelous introduction..."""
      self.window.set_title(msg(1)) # Changing window title.
      box = gtk.VBox(spacing=5)
      box.set_border_width(5)

      for i in range(5, 10):
         label = gtk.Label(msg(i))
         label.set_line_wrap(True)
         box.pack_start(label)

      # Bottom's button.
      box2 = gtk.HBox()
      button = gtk.Button(stock=gtk.STOCK_OK)
      button.connect_object("clicked", self.main,box)
      box2.pack_end(button, False)
      box.pack_start(box2, False)

      # Forget the old box
      self.win_container.remove(oldbox)
      # Then add the new one
      self.win_container.add(box)
      self.win_container.show_all()

   def kana_tables(self, oldbox):
      """Display the full kana tables."""
      self.window.set_title(msg(83))  # Changing window title.
      da_box = gtk.VBox(spacing=4)
      da_box.set_border_width(5)

      label = gtk.Label("%s\n%s" % (msg(93), msg(94)))
      label.set_justify(gtk.JUSTIFY_CENTER)
      da_box.pack_start(label)

      thumb_size = ((26, 23),(32, 20))[self.param['kana_image_theme'] ==
         "kanatest"]

      def button_pressed(widget, event, kind, kana):
         """Update displayed high size kana image and information when a new
            one is pressed.

         """
         if event.type == gtk.gdk.BUTTON_PRESS and event.button == 1:
            # High size kana image.
            image_path = os.path.join(self.datarootpath, "img", "kana",
               self.param['kana_image_theme'], "%s_%s.png" % (("k", "h")\
               [kind], kana))
            kana_image.set_from_file(image_path)

            # Kana transcription.
            transcription = (kana, kanaengine.hepburn_to_other_sys_convert(
               kana, self.param['transcription_system']))[[self.param\
               ['transcription_system']] != "hepburn"]
            if transcription[-2:] == "-2": transcription = transcription[:-2]
            kana_transcription_label.set_text(transcription.upper())

            # Playing kana proununciation.
            if kana[-2:] == "-2": kana = kana[:-2]
            gtk.gdk.threads_enter()
            self.playsound.play_kana(kana, self.param['kana_pronouncing'])
            gtk.gdk.threads_leave()

            # Packing box with kana transcription and pronoucing button, if not
            # yet performed.
            if len(kana_info_box.get_children()) < 2:
               kana_info_box.pack_start(kana_info_event_box)
               kana_info_box.show_all()

      def item(kind, kana):
         """Return a contaier with a small kana image widget associated with
            its transcription label, to put in the kana tables.

         """
         image = gtk.Image()

         # Loading kana PNG image.
         image_path = os.path.join(self.datarootpath, "img", "kana",
            self.param['kana_image_theme'], "%s_%s.png" % (("k", "h")\
            [kind], kana))
         pixbuf = gtk.gdk.pixbuf_new_from_file(image_path)

         # Resizing.
         scaled_buf = pixbuf.scale_simple(thumb_size[0], thumb_size[1],
            gtk.gdk.INTERP_TILES)

         # Updating kana image widget.
         image.set_from_pixbuf(scaled_buf)
         box = gtk.VBox()
         box.pack_start(image)

         # Transcription label.
         transcription = (kana, kanaengine.hepburn_to_other_sys_convert(
            kana, self.param['transcription_system']))[[self.param\
            ['transcription_system']] != "hepburn"]
         if transcription[-2:] == "-2": transcription = transcription[:-2]
         label = gtk.Label(transcription)
         box.pack_start(label)

         container = gtk.EventBox()
         container.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
         container.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.color_parse("white"))
         container.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.color_parse("white"))
         container.connect("button_press_event", button_pressed, kind, kana)
         container.add(box)

         return container

      def portion_selection(widget, portion):
         """Update the portion selection temporary variable value."""
         portion.active = (0, 1)[widget.get_active()]

      def valided_changes(*args):
         for set in kanaengine.hiragana.setsInOrder() +\
            kanaengine.katakana.setsInOrder():
            activity = [x.active + 0 for x in set.portions]
            self.param[set.optionKey] = ('false', 'true')[1 in activity]
            self.param[set.optionKey + "_portions"] = tuple(activity)

         # Updating the whole configuration.
         self.param.write()

         self.main(da_box)  # Going back to the main window.

      da_table = gtk.Table(3, 3, False)
      da_table.set_col_spacings(8)
      da_table.set_row_spacings(4)
      da_box.pack_start(da_table)

      # Vertical separation bar between Hiragana / Katakana.
      da_table.attach(gtk.VSeparator(), 1, 2, 0, 3)
      kana_info_box = gtk.VBox()
      # High-size kana display.
      kana_image = gtk.Image()
      kana_image.set_from_file(os.path.join(self.datarootpath, "img",
         "kana_teacher.png"))
      kana_info_box.pack_start(kana_image, False)
      box2 = gtk.HBox()
      kana_transcription_label = gtk.Label()
      kana_transcription_label.modify_font(FontDescription("sans 22"))
      box2.pack_start(kana_transcription_label)
      kana_info_event_box = gtk.EventBox()
      kana_info_event_box.modify_bg(gtk.STATE_NORMAL,
         gtk.gdk.color_parse("white"))
      kana_info_event_box.add(box2)
      da_table.attach(kana_info_box, 3, 4, 0, 1)

      # Generating kana tables (one per set).
      size = ((6, 10), (6, 5), (4, 10), (6, 10), (6, 5), (4, 10), (6, 5))
      table_coord = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (2, 0), 4: (2, 1),
         5: (2, 2), 6: (3, 1)}
      special_coord = {
         # Basic hiragana / katakana.
         "ya": (8, 1), "yu": (8, 3), "yo": (8, 5), "wa": (9, 1), "o-2":
         (9, 3), "n": (9, 5),
         # Additional katakana.
         "wi": (0, 2), "we": (0, 4), "wo": (0, 5), "kwa": (0, 6), "kwo":
         (0, 7), "gwa": (0, 8), "she": (1, 6), "je": (1, 7), "che": (1, 8),
         "tsa": (1, 1), "tse": (1, 4), "tso": (1, 5), "ti": (2, 2), "tu":
         (2, 3), "tyu": (2, 5), "di": (3, 2), "du": (3, 3), "dyu":
         (3, 5), "ye": (4, 6), "fa": (4, 1), "fi": (4, 2), "fe": (4, 4),
         "fo": (4, 5), "va": (5, 1), "vi": (5, 2), "vu": (5, 3), "ve":
         (5, 4), "vo": (5, 5)}

      def gen_kana_set_table(widget=None, set_num=0):
         if not set_num in (0,3) and not set_container[set_num]\
            .get_child() == None:
            return True

         set = (kanaengine.hiragana.setsInOrder() +\
            kanaengine.katakana.setsInOrder())[set_num]

         table = gtk.Table(size[set_num][0], size[set_num][1])
         table.set_col_spacings(2)
         table.set_row_spacings(1)
         if set_num == 6: table.set_row_spacing(4, 12)

         i = 0
         for portion in set.portions:
            # Portion selection checkbutton.
            frame = gtk.Frame()
            checkbutt = gtk.CheckButton()
            if portion.active:
               checkbutt.set_active(True)
            checkbutt.connect("toggled", portion_selection, portion)
            frame.add(checkbutt)
            x = i
            x_end = x + 1
            if set_num in (0, 3) and i == 8:
               x_end = x + 2
            elif set_num in (2, 5):
               x_end = x + (2, 3)[i == 8]
            elif set_num == 6 and i >= 2:
               if i == 2: x_end = x + 2
               else:
                  x = i + 1
                  x_end = x + 1
            table.attach(frame, x, x_end, 0, 1)

            # Portion's kana.
            j = 1
            for member in portion.members:
               kana = member.kana

               if set_num == 0 or set_num == 3:
                  if i < 8: x, y = i, j
                  else: x, y = special_coord[kana]
               elif set_num == 1 or set_num == 4: x, y = i, j
               elif set_num == 2 or set_num == 5:
                  if j == 4: i += 1; j = 1
                  x, y = i, j
               elif set_num == 6: x, y = special_coord[kana]

               table.attach(item((0, 1)[set_num < 3], kana), x, x + 1, y,
                  y + 1)
               j += 1
            i += 1

         # Packing the table.
         if set_num in (0, 3): set_container[set_num].pack_start(table)
         else:
            set_container[set_num].add(table)
            set_container[set_num].show_all()

      set_container = []
      for i in range(7):
         label = gtk.Label("<b>%s</b>" % msg(30 + (i, i - 3)[i > 2]))
         label.set_use_markup(True)

         if i in (0, 3):
            set_container.append(gtk.VBox())
            kana_kind_label = gtk.Label(msg((28, 29)[i == 3]))
            kana_kind_label.modify_font(FontDescription("bold 14"))
            kana_kind_label.modify_fg(gtk.STATE_NORMAL,
               gtk.gdk.color_parse(("#cc432b", "#2e4898")[i == 3]))

            set_container[i].pack_start(kana_kind_label, padding=2)
            set_container[i].pack_start(label)
         else:
            set_container.append(gtk.Expander())
            set_container[i].set_label_widget(label)
            set_container[i].set_expanded(False)
            set_container[i].connect("activate", gen_kana_set_table, i)

         da_table.attach(set_container[i], table_coord[i][0],
            table_coord[i][0] + 1, table_coord[i][1], table_coord[i][1] +\
            (1, 2)[i == 6], xoptions = gtk.SHRINK, yoptions = gtk.SHRINK)

      for i in (0, 3): gen_kana_set_table(set_num=i)

      # Bottom's buttons.
      box = gtk.HBox(spacing=4)
      button = gtk.Button(stock = gtk.STOCK_CANCEL)
      button.connect("clicked", lambda *args: self.main(da_box))
      box.pack_end(button, False)
      button = gtk.Button(stock = gtk.STOCK_SAVE)
      button.connect("clicked", valided_changes)
      box.pack_end(button, False)
      da_box.pack_start(box, False)

      # Forgeting the old box
      self.win_container.remove(oldbox)
      # Then adding the new one
      self.win_container.add(da_box)
      self.win_container.show_all()

   def quiz(self, oldbox):
      # Randomly getting a kana (respecting bellow conditions).
      self.kana = self.kana_engine.randomKana()

      if self.kana:
         self.quizWidget = {}
         box = gtk.HBox(spacing=4)
         box.set_border_width(5)

         box2 = gtk.VBox()

         # Kana image.
         self.widgets['kanaImage'] = gtk.Image()
         kanaKindIndex = self.kana.kind.kindIndex
         self.set_kana_image(self.kana)
         box2.pack_start(self.widgets['kanaImage'], False)

         # Quiz informations.
         self.widgets['quiz_infos'] = {}
         self.widgets['quiz_infos']['questionNumLabel'] = gtk.Label(
            msg(67).format(self.score.get_question_total() + 1,
               self.param['length']))
         self.widgets['quiz_infos']['systemLabel'] = gtk.Label(msg(68) %
            capwords(self.param['transcription_system']))
         box3 = gtk.VBox(spacing=2)
         box3.pack_start(self.widgets['quiz_infos']['questionNumLabel'])
         box3.pack_start(self.widgets['quiz_infos']['systemLabel'])
         box2.pack_start(box3)
         self.widgets['quiz_infos']['container'] = gtk.EventBox()
         self.widgets['quiz_infos']['container'].modify_bg(gtk.STATE_NORMAL,
            gtk.gdk.color_parse("white"))
         self.widgets['quiz_infos']['container'].add(box2)
         box.pack_start(self.widgets['quiz_infos']['container'], False)

         self.widgets['quiz_right_box'] = gtk.VBox(spacing=4)
         if self.param["kana_image_scale"] == "small": width = 120
         elif self.param["kana_image_scale"] == "medium": width = 175
         else: width = 250
         self.widgets['quiz_right_box'].set_size_request(width, -1)

         # Stop button.
         self.widgets['quiz_stop'] = gtk.Button(stock=gtk.STOCK_STOP)
         self.widgets['quiz_stop'].connect("clicked", self.results)
         self.widgets['quiz_right_box'].pack_start(self.widgets['quiz_stop'],
            False)
         # Question label.
         self.widgets['quiz_label'] = gtk.Label((msg(11), msg(12))[
            self.kana.kind.kindIndex])
         self.widgets['quiz_label'].set_justify(gtk.JUSTIFY_CENTER)
         self.widgets['quiz_label'].set_line_wrap(True)
         self.widgets['quiz_right_box'].pack_start(self.widgets['quiz_label'])

         # The ``next" button.
         self.widgets['next_button'] = gtk.Button()
         self.widgets['next_button'].add(gtk.Arrow(gtk.ARROW_RIGHT,
            gtk.SHADOW_IN))

         if self.param['answering_mode'] == "list":
            # Choice buttons generation.
            self.widgets['random_ans_butt'] = []
            self.widgets['random_ans_kana_label'] = []
            for i in range(self.param['list_size']):
               self.widgets['random_ans_butt'].append(gtk.Button())
               butt_box = gtk.HBox()
               label = gtk.Label(str(i + 1))
               butt_box.pack_start(label, False)
               self.widgets['random_ans_kana_label'].append(gtk.Label())
               self.widgets['random_ans_kana_label'][i].modify_font(
                  FontDescription("sans 19"))
               butt_box.pack_start(self.widgets['random_ans_kana_label']\
                  [i])
               self.widgets['random_ans_butt'][i].add(butt_box)
               self.widgets['random_ans_butt'][i].connect("clicked",
                  self.check_answer, i)
               self.widgets['quiz_right_box'].pack_start(self.widgets\
                  ['random_ans_butt'][i])

            self.display_random_list()

            self.handlerid['nextbutton_clicked'] = self.widgets['next_button']\
               .connect("clicked", self.new_question)
         else:
            entry = gtk.Entry(3)
            entry.modify_font(FontDescription("sans 35"))
            entry.set_alignment(0.5)
            entry.set_width_chars(3)
            entry.connect("changed", lambda widget: widget.set_text(
               widget.get_text().upper()))
            self.widgets['quiz_right_box'].pack_start(entry)

            self.handlerid['nextbutton_clicked'] = self.widgets['next_button'].\
               connect_object("clicked", self.check_answer, entry)
            entry.connect("activate", lambda widget:
               self.widgets['next_button'].clicked())

         self.widgets['quiz_right_box'].pack_start(self.widgets['next_button'])
         box.pack_end(self.widgets['quiz_right_box'])

         # Forgetting the old box.
         self.win_container.remove(oldbox)
         # Then addding the new one.
         self.win_container.add(box)
         self.win_container.show_all()

         # Hidding the arrow.
         if self.param['answering_mode'] == "list":
            self.widgets['next_button'].hide()
         else: entry.grab_focus()  # Bringing focus to text entry.

         self.widgets['quiz_stop'].hide()  # Hidding the stop button.

      else:
         dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
            gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, msg(60))
         dialog.connect('response', lambda dialog, response: dialog.destroy())
         dialog.show()

   def display_random_list(self):
      possibles_answers = self.kana_engine.randomAnswers(
         self.param['list_size'])
      i = 0
      for answer in possibles_answers:
         x = answer.transcriptions[self.param['transcription_system']]
         if x[-2:] == "-2": x = x[:-2]
         self.widgets['random_ans_kana_label'][i].set_text(x.upper())
         self.widgets['random_ans_butt'][i].show()
         i += 1

   def check_answer(self, widget, num = None):
      """Compare user given answer to the correct one, update the score,
         then display that question result.

      """
      if self.param['answering_mode'] == "list":
         user_answer = self.widgets['random_ans_kana_label'][num].get_text()\
            .lower()
      else: user_answer = widget.get_text().lower()

      # If the selected romanization system is *other* than Hepburn (default),
      # let's convert the good answer (given in the Hepburn internal format)
      # to the user-selected romanization system, in order to compare with its
      # chosen answer.
      correct_answer = self.kana.transcriptions[self.param[\
         'transcription_system']]
      if correct_answer[-2:] == "-2": correct_answer = correct_answer[:-2]

      if user_answer == correct_answer:  # \o/
         self.widgets['quiz_label'].set_text("<span color='darkgreen'><b>"
            "%s</b></span>" % msg(13))
         self.score.update(1)  # Updating the score (add 1 point).
      else:  # /o\
         self.widgets['quiz_label'].set_text("<span color='red'><b>%s</b>"
            "</span>\n%s" % (msg(14), msg(15) % "<big><b>%s</b></big>"\
            % correct_answer.upper()))
         self.score.update(0, correct_answer, self.kana.kind.kindIndex)
      self.widgets['quiz_label'].set_use_markup(True)

      if self.param['answering_mode'] == "list":
         for butt in self.widgets['random_ans_butt']:
            butt.hide()  # Hidding choices buttons.
         self.widgets['next_button'].show()  # Showing the ``next" button.
      else:
         widget.hide()
         self.widgets['next_button'].disconnect(
            self.handlerid['nextbutton_clicked'])
         self.handlerid['nextbutton_clicked'] = self.widgets['next_button']\
            .connect_object("clicked", self.new_question,widget)

      # Bringing focus to the ``next" button.
      self.widgets['next_button'].grab_focus()

      # Playing kana proununciation.
      kana = self.kana.kana
      if kana[-2:] == "-2": kana = kana[:-2]
      gtk.gdk.threads_enter()
      self.playsound.play_kana(kana, self.param['kana_pronouncing'])
      gtk.gdk.threads_leave()

      if self.param['answer_display_timeout'] > 0:
         # Automatic Quiz Proceeding (AQP)feature.
         def countdown():
            i = self.param['answer_display_timeout']
            while i > 0:
               self.widgets['next_button'].remove(self.widgets['next_button']\
                  .get_child())
               self.widgets['next_button'].add(gtk.Label(i))
               self.widgets['next_button'].show_all()
               time.sleep(1)
               i = i - 1
            self.widgets['next_button'].clicked()

         t = threading.Thread(target=countdown)
         t.start()

      if self.score.is_quiz_finished(self.param['length']):
         # The quiz is finished... Let's show results!
         self.widgets['next_button'].disconnect(
            self.handlerid['nextbutton_clicked'])
         self.handlerid['nextbutton_clicked'] = self.widgets['next_button']\
            .connect("clicked", self.results)
      else: self.widgets['quiz_stop'].show()

   def new_question(self, widget):
      # Randomly getting a kana.
      self.kana = self.kana_engine.randomKana()

      # Updating kana's image.
      self.set_kana_image(self.kana)

      self.widgets['quiz_infos']['questionNumLabel'].set_text(
         msg(67).format(self.score.get_question_total() + 1,
            self.param['length']))
      self.widgets['quiz_label'].set_text((msg(11), msg(12))\
         [self.kana.kind.kindIndex])

      if self.param['answering_mode'] == "list":
         self.widgets['next_button'].hide()  # Hidding the ``next" button.
         self.display_random_list()
      else:  # Displaying the text entry.
         widget.set_text("")
         widget.show()
         widget.grab_focus()  # Giving focus to text entry.
         self.widgets['next_button'].disconnect(
            self.handlerid['nextbutton_clicked'])
         self.handlerid['nextbutton_clicked'] = self.widgets['next_button']\
            .connect_object("clicked", self.check_answer, widget)

      self.widgets['quiz_stop'].hide()  # Hidding the stop button.

   def results(self, data):
      """End-time quiz results display."""
      results = self.score.get_results()
      text = u"<big>%s</big>\n\n%s\n%s\n%s" % (msg(16), msg(17) % results[0],
         msg(18) % results[1], msg(19) % results[2])

      def get_unrec_msg(kind):
         """Return a ready-to-display string which indicates the
            unrecognized kana (by kind) during the quiz.

         """
         plop = ""
         for key, val in results[3][kind].items():
            for x in val:
               if key != 1: plop += "%s (%s), " % (x.upper(), key)
               else: plop += u"%s, " % x.upper()
         return "\n%s" % (msg(72 + kind) % plop[:-2])

      if len(results[3][0]) > 0: text += get_unrec_msg(0)
      if len(results[3][1]) > 0: text += get_unrec_msg(1)

      self.widgets['quiz_label'].set_text(text)
      self.widgets['quiz_label'].modify_font(FontDescription("sans 14"))
      self.widgets['quiz_label'].set_use_markup(True)
      self.widgets['quiz_label'].set_line_wrap(True)
      self.widgets['quiz_label'].set_padding(2, 6)

      self.widgets['quiz_right_box'].set_size_request(-1, -1)

      # Reusing kana image & quiz information widgets to display a result
      # image and comment.
      if results[2] <= 40: lvl =0
      elif results[2] <= 60: lvl = 1
      elif results[2] <= 80: lvl = 2
      else: lvl = 3
      self.widgets['kanaImage'].set_from_file(os.path.join(self.datarootpath,
         "img", "results_%s.png" % ("crappy", "average", "good", "excelent")\
         [lvl]))

      self.widgets['quiz_infos']['container'].modify_bg(gtk.STATE_NORMAL,
         gtk.gdk.color_parse("#f3eddd"))
      self.widgets['quiz_infos']['questionNumLabel'].set_text(msg(89 + lvl))
      self.widgets['quiz_infos']['questionNumLabel'].modify_font(
         FontDescription("sans 19"))
      self.widgets['quiz_infos']['systemLabel'].hide()

      self.score.reset()  # Reseting the score.
      self.kana_engine.reset()  # Reseting kana engine's variables.

      if self.param['answer_display_timeout'] > 0:
         self.widgets['next_button'].remove(self.widgets['next_button']\
            .get_child())
         self.widgets['next_button'].add(gtk.Arrow(gtk.ARROW_RIGHT,
            gtk.SHADOW_IN))
         self.widgets['next_button'].show_all()

      self.widgets['next_button'].set_size_request(-1, 80)
      # Directing the ``next" button toward the main window.
      self.widgets['next_button'].disconnect(
         self.handlerid['nextbutton_clicked'])
      self.widgets['next_button'].connect_object("clicked", self.main,
         self.win_container.get_child())
      self.widgets['quiz_stop'].hide()  # Hidding the stop button.

   def options(self, oldbox):
      # Dicts for integrer to string param convertion and vice-versa...
      opt_conv = {
         "boolean": {0: 'false', 1: 'true', 'false': 0, 'true': 1},
         "transcription_system":  {0: 'hepburn', 1: 'kunrei-shiki',
            2: 'nihon-shiki', 3: 'polivanov', 'hepburn': 0,
            'kunrei-shiki': 1, 'nihon-shiki': 2, 'polivanov': 3},
         "answering_mode": {0: 'list', 1: 'entry', 'list': 0, 'entry': 1},
         "rand_answer_sel_range": {0: 'portion', 1: 'set', 2: 'kind',
            'portion': 0, 'set': 1, 'kind': 2},
         "kana_image_scale": {0: 'small', 1: 'medium', 2: 'large',
            'small': 0, 'medium': 1, 'large': 2},
         "kana_image_theme": {0: 'choplair', 1: 'kanatest',
            'choplair': 0, 'kanatest': 1},
         "kana_pronouncing": {0: 'female', 1: 'male', 2: 'alternate',
            'female': 0, 'male': 1, 'alternate': 2},
         "lang": {0: 'en', 1: 'fr', 2: 'gl', 3: 'de', 4: 'pt_BR',
            5: 'ru', 6: 'sr', 7: 'es', 8: 'sv', 'en': 0, 'fr': 1,
            'gl': 2, 'de': 3, 'pt_BR': 4, 'ru': 5, 'sr': 6, 'es': 7,
            'sv': 8}
         }

      def callback(widget, special=None):
         if special == "save":
            self.param['transcription_system'] = opt_conv\
               ["transcription_system"][opt_widget['transcription_system']\
               .get_active()]
            self.param['answering_mode'] = opt_conv["answering_mode"]\
               [opt_widget['answering_mode'].get_active()]
            self.param['list_size'] = opt_widget['list_size'].get_active()\
               + 2
            self.param['rand_answer_sel_range'] = opt_conv\
               ["rand_answer_sel_range"][opt_widget\
               ["rand_answer_sel_range"].get_active()]
            self.param['length'] = int(opt_widget['length'].get_value())
            self.param['kana_no_repeat'] = opt_conv["boolean"][opt_widget\
               ['kana_no_repeat'].get_active()]
            self.param['kana_image_scale'] = opt_conv["kana_image_scale"]\
               [opt_widget["kana_image_scale"].get_active()]
            self.param['kana_image_theme'] = opt_conv["kana_image_theme"]\
               [opt_widget["kana_image_theme"].get_active()]
            self.param['kana_pronouncing'] = opt_conv["kana_pronouncing"]\
               [opt_widget["kana_pronouncing"].get_active()]

            # Language has been changed: tell that restart needed for this
            # change to take effect.
            if self.param['lang'] != opt_conv["lang"][opt_widget['lang']\
              .get_active()]:
              dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
              gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, msg(114))
              dialog.connect('response', lambda dialog, response:
               dialog.destroy())
              dialog.show()



            self.param['lang'] = opt_conv["lang"][opt_widget['lang']\
               .get_active()]

            # Updating the whole configuration.
            self.param.write()
         self.main(da_box)  # Going back to the ``main".

      self.window.set_title(msg(2))  # Changing window's title.
      da_box = gtk.HBox(spacing=3)
      da_box.set_border_width(5)

   #   toolbar = gtk.Toolbar()
   #   toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)
   #   toolbar.set_style(gtk.TOOLBAR_BOTH)
   #   for i in range(83, 87):
   #      button = gtk.Button(msg(i))
   #      item = gtk.ToolItem()
   #      item.add(button)
   #      item.set_expand(True)
   #      item.set_homogeneous(True)
   #      toolbar.insert(item, i - 83)
   #   da_box.pack_start(toolbar)
      box = gtk.VBox(spacing=3)
      da_box.pack_start(box)

      label = gtk.Label(msg(20))
      box.pack_start(label, False)
      box2 = gtk.HBox()
      box.pack_start(box2)

      box3 = gtk.VBox(spacing=2)
      box3.set_border_width(6)
      box2.pack_start(box3)

      opt_widget = {}

      # `transcription_system'
      label = gtk.Label(msg(61))
      box3.pack_start(label)
      opt_widget['transcription_system'] = gtk.combo_box_new_text()
      for x in (62, 63, 64, 79):
         opt_widget['transcription_system'].append_text(msg(x))
      opt_widget['transcription_system'].set_active(opt_conv\
         ["transcription_system"][self.param['transcription_system']])
      box3.pack_start(opt_widget['transcription_system'])

      # `answering_mode'
      label = gtk.Label(msg(38))
      box3.pack_start(label)
      opt_widget['answering_mode'] = gtk.combo_box_new_text()
      for x in (39, 40):
         opt_widget['answering_mode'].append_text(msg(x))
      opt_widget['answering_mode'].set_active(opt_conv["answering_mode"]\
         [self.param['answering_mode']])
      box3.pack_start(opt_widget['answering_mode'])

      # `list_size'
      label = gtk.Label(msg(41))
      box3.pack_start(label)
      opt_widget['list_size'] = gtk.combo_box_new_text()
      for x in (2, 3, 4, 5):
         opt_widget['list_size'].append_text(msg(42) % x)
      opt_widget['list_size'].set_active(self.param['list_size'] - 2)
      box3.pack_start(opt_widget['list_size'])

      # `rand_answer_sel_range'
      label2 = gtk.Label(msg(75))
      box3.pack_start(label2)
      opt_widget['rand_answer_sel_range'] = gtk.combo_box_new_text()
      for x in (76, 77, 78):
         opt_widget['rand_answer_sel_range'].append_text(msg(x))
      opt_widget['rand_answer_sel_range'].set_active(opt_conv[
         "rand_answer_sel_range"][self.param['rand_answer_sel_range']])
      box3.pack_start(opt_widget['rand_answer_sel_range'])

      # Bouyaka!
      def bouyaka(widget,targets):
         """Set list size widgets sensitive state according
            to answer mode widget selected param.

         """
         for x in targets: x.set_sensitive(not widget.get_active())

      bouyaka(opt_widget['answering_mode'], (label, opt_widget['list_size'],
         label2, opt_widget['rand_answer_sel_range']))
      opt_widget['answering_mode'].connect("changed", bouyaka, (label,
         opt_widget['list_size'], label2, opt_widget[
         'rand_answer_sel_range']))

      # `length'
      box4 = gtk.HBox()
      label = gtk.Label(msg(43))
      box4.pack_start(label)
      adjustment = gtk.Adjustment(float(self.param['length']), 1,
         200, 1, 10)
      opt_widget['length'] = gtk.SpinButton(adjustment)
      opt_widget['length'].set_alignment(0.5)
      box4.pack_start(opt_widget['length'])
      box4.pack_end(gtk.Label(msg(80)), False)
      box3.pack_start(box4)

      # `kana_no_repeat'
      opt_widget['kana_no_repeat'] = gtk.CheckButton(msg(44))
      opt_widget['kana_no_repeat'].set_active(opt_conv["boolean"]\
         [self.param['kana_no_repeat']])
      box3.pack_start(opt_widget['kana_no_repeat'])

      # `kana_image_scale'
      box4 = gtk.HBox()
      label = gtk.Label(msg(95))
      box4.pack_start(label)
      opt_widget['kana_image_scale'] = gtk.combo_box_new_text()
      for x in (96, 97, 98):
         opt_widget['kana_image_scale'].append_text(msg(x))
      opt_widget['kana_image_scale'].set_active(opt_conv["kana_image_scale"]\
         [self.param['kana_image_scale']])
      box4.pack_start(opt_widget['kana_image_scale'])
      box3.pack_start(box4)

      # `kana_image_theme'
      label = gtk.Label(msg(99))
      box3.pack_start(label)
      opt_widget['kana_image_theme'] = gtk.combo_box_new_text()
      for x in (100, 101):
         opt_widget['kana_image_theme'].append_text(msg(x))
      opt_widget['kana_image_theme'].set_active(opt_conv["kana_image_theme"]\
         [self.param['kana_image_theme']])
      box3.pack_start(opt_widget['kana_image_theme'])

      # `kana_pronouncing'
      label = gtk.Label(msg(108))
      box3.pack_start(label)
      opt_widget['kana_pronouncing'] = gtk.combo_box_new_text()
      for x in (109, 110, 111):
         opt_widget['kana_pronouncing'].append_text(msg(x))
      opt_widget['kana_pronouncing'].set_active(opt_conv["kana_pronouncing"]\
         [self.param['kana_pronouncing']])
      box3.pack_start(opt_widget['kana_pronouncing'])

      # `lang'
      box4 = gtk.HBox()
      label = gtk.Label(msg(45))
      box4.pack_start(label)
      opt_widget['lang'] = gtk.combo_box_new_text()
      for x in (46, 47, 113, 70, 48, 74, 49, 112, 50):
         opt_widget['lang'].append_text(msg(x))
      opt_widget['lang'].set_active(opt_conv["lang"][self.param['lang']])
      box4.pack_start(opt_widget['lang'])
      box3.pack_start(box4)

      # Bottom's buttons.
      box2 = gtk.HBox()
      button = gtk.Button(stock=gtk.STOCK_CANCEL)
      button.connect("clicked", callback)
      box2.pack_end(button, False)
      button = gtk.Button(stock=gtk.STOCK_SAVE)
      button.connect("clicked", callback, "save")
      box2.pack_end(button, False)
      box.pack_end(box2,False)

      # Remove the old box then add the new one.
      self.win_container.remove(oldbox)
      self.win_container.add(da_box)
      self.win_container.show_all()

   def about(self, oldbox):
      """Display the About dialog."""
      self.window.set_title(msg(4))  # Changing window title.
      da_box = gtk.VBox(spacing=4)
      da_box.set_border_width(5)

      box = gtk.HBox(spacing=6)
      image = gtk.Image()
      image.set_from_file(os.path.join(self.datarootpath, "img", "icon.png"))
      box.pack_start(image)
      box2 = gtk.VBox()
      label = gtk.Label("<span color='#008'><b>%s</b>\n%s</span>" %
         (msg(53), msg(54) % self.version))
      label.set_justify(gtk.JUSTIFY_CENTER)
      label.set_use_markup(True)
      box2.pack_start(label)
      label = gtk.Label("Copyleft 2003, 2004, 2005, 2006, 2007, "\
         "2008, 2009 Choplair Organization")
      box2.pack_start(label)
      box.pack_start(box2)
      da_box.pack_start(box)

      licence_label = gtk.Label(msg(55))
      licence_label.set_justify(gtk.JUSTIFY_CENTER)
      licence_label.set_size_request(480, -1)
      licence_label.set_line_wrap(True)
      da_box.pack_start(licence_label)

      frame = gtk.Frame(msg(56))
      container = gtk.EventBox()
      container.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#c9ddff"))
      box = gtk.HBox(spacing=2)
      box.set_border_width(3)

      box2 = gtk.VBox()
      logo = gtk.Image()
      logo.set_from_file(os.path.join(self.datarootpath, "img", "chprod.png"))
      box2.pack_start(logo)
      label = gtk.Label("<i>http://www.choplair.org/</i>")
      label.set_selectable(True)
      label.set_use_markup(True)
      box2.pack_start(label)
      box.pack_start(box2, padding=4)

      for i in (0, 1):
         buffer = gtk.TextBuffer()
         buffer.set_text(("%s\n%s\n\n%s\n%s" % (msg(66), msg(57), msg(81),
            msg(82)), "%s\n%s\n\n%s\n%s\n\n%s\n%s" % (msg(102), msg(103),
            msg(104), msg(105), msg(106), msg(107)))[i])
         buffer.apply_tag(buffer.create_tag(justification=gtk.JUSTIFY_CENTER,
            editable=False), buffer.get_start_iter(), buffer.get_end_iter())
         for x in ((0, 4), (0, 4, 9))[i]:
            buffer.apply_tag(buffer.create_tag(weight=700),
               buffer.get_iter_at_line(x), buffer.get_iter_at_line(x + 1))
         textview = gtk.TextView(buffer)
         textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#c9ddff"))
         box.pack_start(textview)

      container.add(box)
      frame.add(container)

      da_box.pack_start(frame)

      # Bottom's buttons.
      box = gtk.HBox()
      button = gtk.Button(stock = gtk.STOCK_CLOSE)
      button.connect("clicked", lambda *args: self.main(da_box))
      box.pack_end(button, False)
      da_box.pack_start(box, False)

      # Forgeting the old box
      self.win_container.remove(oldbox)
      # Then adding the new one
      self.win_container.add(da_box)
      self.win_container.show_all()

   def set_kana_image(self, kana):
      """Updating kana image."""
      kind = kana.kind.kindIndex
      kana = kana.kana # the string

      # Loading kana PNG image.
      pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(self.datarootpath,
         "img", "kana", self.param['kana_image_theme'], "%s_%s.png" %
         (("k", "h")[kind], kana)))

      # Scaling image buffer according to user size preference.
      if self.param["kana_image_scale"] == "small":
         width = (150, 225)[self.param['kana_image_theme'] == "kanatest"]
      elif self.param["kana_image_scale"] == "medium":
         width = (210, 325)[self.param['kana_image_theme'] == "kanatest"]
      else:
         width = (330, 495)[self.param['kana_image_theme'] == "kanatest"]
      # Corresponding height.
      height = pixbuf.get_height() * width / pixbuf.get_width()
      scaled_buf = pixbuf.scale_simple(width, height, gtk.gdk.INTERP_HYPER)

      # Updating kana image widget.
      self.widgets['kanaImage'].set_from_pixbuf(scaled_buf)

   def quit(self,widget):
      gtk.main_quit()  # Ja mata~~

