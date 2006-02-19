#!/usr/bin/env python
from distutils.core import setup
import os

def filelist(dir):
	"""Return (not recursively) the relative path of all *files* in a directory."""
	list = []
	for x in os.listdir(dir):
		rel_path = os.path.join(dir,x)
		if os.path.isfile(rel_path):
			list.append(rel_path)
	return list

setup(
	name='Kana no quiz',
	version='1.4b',
	description='A kana memorization tool.',
	author='Choplair-network',
	author_email='contact@choplair.org',
	url='http://www.choplair.org/',
	download_url='http://developer.berlios.de/project/filelist.php?group_id=1783',
	license='GNU General Public License',
	packages=['kana-no-quiz'],
	package_dir={'kana-no-quiz': 'data/py'},
	data_files=[
		#Images.
		('share/kana-no-quiz/img',filelist("data/img")),
		('share/kana-no-quiz/img/kana',filelist("data/img/kana")),
		#Localisation.
		('share/kana-no-quiz/locale',['data/locale/kana-no-quiz.pot']),
		('share/kana-no-quiz/locale/fr/LC_MESSAGES',filelist('data/locale/fr/LC_MESSAGES')), #French
		('share/kana-no-quiz/locale/pt_BR/LC_MESSAGES',filelist('data/locale/pt_BR/LC_MESSAGES')), #Portuguese of Brazil
		('share/kana-no-quiz/locale/sr/LC_MESSAGES',filelist('data/locale/sr/LC_MESSAGES')), #Serbian
		('share/kana-no-quiz/locale/sv/LC_MESSAGES',filelist('data/locale/sv/LC_MESSAGES'))] #Swedish
	)
