
 Kana no quiz - README
 version 1.0 - 2004-06-XX
~~~~~~~~~~~~~~~~~~~~~~~~~~

 Introduction
 ============

 This is ``Kana no quiz", a little tool, written in Python,
to memorize Japanese kana (hiragana & katakana).

The method is quite simple: kana appear randomly and you
have to find their romaji transcription (Hepburn). There are
several possibilities, but only one anwser is right!

 I18n
 ----

 Kana no quiz is currently translated into English, French
and Swedish (thanks to Markus Fellnert).

 Cross platform
 --------------

 The same package works both on GNU/Linux (using GTK+) and
Windows (using the Python native GUI: Tkinter). You can force
an interface by passing the `-tk' (for Tkinter) or `-gtk' (for
GTK+) argument.

 GIF choice
 ----------

 Why do we use images in the GIF format to render kana?
GIF is evil! Ok, but the Tkinter interface accept neither
PNG nor JPG. So we must use GIF for compatibility...


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
* For the GTK+ interface (not mandatory to run on Windows):
  * The Gimp Tool Kit - http://www.gtk.org/.
  * PyGTK - http://www.pygtk.org/.


 Stay tuned
 ==========

 Kana no quiz is a project of the Choplair-network, you can
get information and update from our website:
	http://www.choplair.org/ 


 That's all for now, have fun ;)
