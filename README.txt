
 Kana no quiz - README
 version 1.4b - 2006-01-01
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Introduction
 ============

 This is ``Kana no quiz", a little educational tool, written
in Python, to memorize Japanese kana (hiragana & katakana)
pronouncing in an easy way.

 The full list of kana is implemented, including additional
katakana used in modern language. Default used romanization
system is the Hepburn's (most common world-wide), but it does
also support Kunrei and Nihon-shiki systems.

 This program is cross platform, the same package works both
on GNU/Linux and Windows.

 How does it work?
 -----------------

 The method is quite simple: a kana appear randomly and you
have to find its romaji transcription; either by choosing the
good answer from a random list containing several possibili-
ties or by directly typing the answer through a text entry.
This second method of course is more complicated.

 Progressive learning
 --------------------
 
 Through its option panel, Kana no quiz allows you to tune up
the quiz precisely, like choosing which group of kana you want
to train yourself upon.

 First, hiragana and katakana are separated, both are then di-
vided into big sets of kana according to their type (``Basic",
``Modified", ``Combined"; and a special ``Additional" set for
katakana only) which are thus composed of various portions
containing 5/6 kana, following the traditional alphabet order
(i.e.: ``ka ki ku ke ko").

 According to your need and level, you may select one or more
portions of the same or different sets, whole sets, all the
kana... Once you feel comfortable (you can check it with the
results displayed at the end of each quiz), you may also
increase the number of possible answers in the random list,
or even choose to answer directly through the text entry.
Difficulty can be adapted to your skill: this is progressive
learning.

 From the complete beginner who has to start easily and learn
step by step, to the wizard who just wants to confirm his/her
absolute master of the kana, everyone should get satisfated
with Kana no quiz!


 Dependencies
 ============

 To run fine, Kana no quiz requires the following softwares
to be installed on your computer:

* Python - `http://www.python.org/'.
* For the GTK+ interface (not mandatory but recommanded):
  * The Gimp Tool Kit - `http://www.gtk.org/'.
  * PyGTK - `http://www.pygtk.org/'.


 Launching
 =========

 I guess it should be clear for most of people, but in order
to launch Kana no quiz, you just have to execute the file
`kana-no-quiz.py'.

 On Windows, it is simply done by double-clicking on it.
 
 On GNU/Linux, you can go to Kana-no-quiz directory using your
favorite graphical shell, then type `python kana-no-quiz.py'.


 Some details
 ============

 I18n
 ----

 Thanks to our contributors, Kana no quiz is currently
translated into English, French, Portuguese of Brazil (by
Matheus Villela), Serbian (by Dejan Danilović) and Swedish (by
Markus Fellnert). Feel free to help that list growing up!

 Multiple interfaces
 -------------------

 Kana-no-quiz may be displayed using two different interface
types, GTK+ or the Python native GUI: Tkinter. The second one
has been introduced to reduce the chore of installing many
dependencies, especialy for Windows users who may already feel
borred by installing Python.

 Although there is not huge differences, the GTK+ interface is
still the most evolved (and the nicest!) and is recommended to
use, but requires some more dependencies (see bellow).

 If possible (satisfated dependencies), the GTK+ interface is
choosen by default. Anyway, you can force the use of an
interface by passing either `-tk' (for Tkinter) or `-gtk' (for
GTK+) as an argument when launching the program.

 The interface type used by Kana no quiz is indicated in the
``About" window, after the version number.

 GIF choice
 ----------

 Why do we use images in the GIF format to render kana?
GIF is evil! Ok, but the Tkinter interface doesn't accept
either PNG or JPG. Thus we must use GIF for the sake of compa-
tibility...

 Kana image sources
 ------------------
 
 The kana images are bitmap exports of SVG files we modelized
by ourselves, using Inkscape, with the hope they could also be
reused for other purposes, by people who enjoy them. So, the
source SVGs have been made publicly available (see our
website), under the conditions indicated above.


 Licensing
 =========

 Kana no quiz is free software released under the GNU GPL 
license (see `GPL.txt'). Kana images are released under the
Free Art license (see `FAL.txt'), as the Kana no quiz logo.


 Stay tuned
 ==========

 Kana no quiz is a project conducted by the Choplair-network,
you can get lastest information and update from our website:
	`http://www.choplair.org/'


 That's all for now, have fun. ;)
	Choplair
