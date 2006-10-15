
 Kana no quiz - README
 version 1.7 - 2006-10-15
~~~~~~~~~~~~~~~~~~~~~~~~~~

 Introduction
 ============

 This is ``Kana no quiz", a little educational tool, written
in Python, to memorize Japanese kana (hiragana & katakana)
pronounciation in an easy way, and thus accomplish the first
step in learning the language.

 The full list of kana is implemented, including additional
katakana used in modern language. Default used transcription
system is the Hepburn's (most common world-wide), but it does
also support Kunrei-shiki, Nihon-shiki and Polivanov systems.

 This program is cross platform, the same package works on
GNU/Linux, FreeBSD, MacOSX and Windows, using the same GTK+
interface on every platform.

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


 Use Kana-no-quiz
 ================

 Prerequisites
 -------------

 To run fine, Kana no quiz requires the following softwares
to be priorly installed on your computer:

* Python - `http://www.python.org/'.
* For the GTK+ interface:
  * The Gimp Tool Kit - `http://www.gtk.org/'.
  * PyGTK - `http://www.pygtk.org/'.

Optional: Psyco module, to increase speed performance.

 Program installation
 --------------------
 
 This process depends on your package type and platform.

 On Windows, simply install Kana-no-quiz using the graphical,
binary installer

 On GNU/Linux, like other Unixes, if not using any distro-
specific package but the classic source code, simply enter 
`python setup.py install' as root to install Kana-no-quiz.

 Launching
 ---------

 On Windows, just click on the shortcut created in the
Start Menu.

 On GNU/Linux, simply enter the `kana-no-quiz' command.

 Enjoy. ;)

 Some details
 ============

 I18n
 ----

 Thanks to our contributors, Kana no quiz is currently
translated into English, French, German (by Florian Niemann),
Portuguese of Brazil (by Matheus Villela), Russian (by Aleksej
R. Serdyukov), Serbian (by Dejan Danilović) and Swedish (by
Markus Fellnert). Feel free to help that list growing up!

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
