# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

#http://www.py2exe.org/index.cgi/CustomIcons
#http://www.winterdrache.de/freeware/png2ico/

from distutils.core import setup
import py2exe
import sys
sys.argv.append('py2exe')

#setup(windows=["encode.py"], options={"py2exe" : {"includes" : ["sip", "PyQt4", "youtube_dl"]}})

setup(
	name = 'BWXRef',
	version='0.5',
	description='BibleWorks XRef to Kor Converter',
	author='Uisang Hwang',
    #data_files = [("kbible_path.txt")],
	#windows=[{"script": 'bwxref_gui.py', "icon_resources": [(0, "bwxref.ico")]}], 
	windows=[{"script": 'bwxref_gui.py', "icon_resources": [(0, "bwxref.ico")],"dest_base": "bwxref"}], 
	options={'py2exe': {"dist_dir": "bin", "includes" : ["sip", "PyQt4"], "excludes":["TKinter"]}} 
)