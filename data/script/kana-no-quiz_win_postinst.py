"""
Kana no quiz!
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

#This script is based on the one found in the ``Kofoto" package.
import sys

if sys.platform[:3] != "win":
    sys.exit()

if sys.argv[1] == "-install":
    import os.path

    #Creating a Start Menu shortcut to a Kana no quiz init script
    #with the `.pyw', so that the program will be lauched without
    #displaying the background console.
    target = os.path.join(sys.prefix,"Scripts","kana-no-quiz_start.pyw")
    try:
        programs_dir = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
    except OSError:
        try:
            programs_dir = get_special_folder_path("CSIDL_PROGRAMS")
        except OSError, reason:
            print "Couldn't install shortcuts: %s" % reason
            sys.exit()
    programs_shortcut = os.path.join(programs_dir, "Kana no quiz.lnk")

    create_shortcut(target,"A kana memorization tool.",programs_shortcut,"","",
        os.path.join(sys.prefix,'share','kana-no-quiz','img','icon.png'))
    file_created(programs_shortcut)

    print "Created Kana no quiz shortcut in the Start menu.\n You're done!"
