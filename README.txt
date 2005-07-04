
 Kana no quiz - README
 version 1.3 - 2005-XX-XX
~~~~~~~~~~~~~~~~~~~~~~~~~~

 Introduction
 ============

 This is ``Kana no quiz", a little educational tool, written
in Python, to memorize Japanese kana (hiragana & katakana)
pronouncing. The full list of kana is implemented, including
additional katakana used in modern language. The romanization
system used is the Hepburn's.

 How does it work ?
 ------------------

 The method is quite simple: a kana appear randomly and you
have to find its romaji transcription; either by choosing the
good answer from a random list containing several possibilities
or by directly typing the answer through a text entry. This
second method is more complicated.

 I18n
 ----

 Kana no quiz is currently translated into English, French,
Portuguese of Brazil (by Matheus Villela), Serbian (by Dejan
Danilović) and Swedish (by Markus Fellnert & Krister
Kjellstrom).

 Cross platform
 --------------

 The same package works both on GNU/Linux and Windows
using GTK+ or the Python native GUI: Tkinter. You can force
the use of an interface by passing either `-tk' (for Tkinter)
or `-gtk' (for GTK+) as an argument. Though there is not much
difference, the GTK+ interface is more evolved (and nicer !),
but you'll need to install some more software to use it (see
bellow). The interface type used by Kana no quiz is indicated
in the ``About" window.

 GIF choice
 ----------

 Why do we use images in the GIF format to render kana?
GIF is evil! Ok, but the Tkinter interface doesn't accept
either PNG or JPG. Thus we must use GIF for the sake of compa-
tibility...


 Licensing
 =========

 Kana no quiz is free software released under the GNU GPL 
license (see `GPL.txt'). Kana images are released under the
Free Art license (see `FAL.txt'), as the Kana no quiz logo.


 Dependencies
 ============

 Kana no quiz requires the following softwares installed on
your computer:

* Python - http://www.python.org/.
* For the GTK+ interface (not mandatory but recommanded):
  * The Gimp Tool Kit - http://www.gtk.org/.
  * PyGTK - http://www.pygtk.org/.


 Stay tuned
 ==========

 Kana no quiz is a project conducted by the Choplair-network,
you can get information and update from our website:
	`http://www.choplair.org/'


 That's all for now, have fun ;)
