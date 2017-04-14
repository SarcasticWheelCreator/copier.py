#!/usr/bin/env python
#coding=utf-8

import shutil
import sys
from os.path import join, exists, splitext

try:		
	import xml.etree.cElementTree as xml_tree
except ImportError:
	import xml.etree.ElementTree as xml_tree

manual = """
Wrong parameters.\n
Usage: \"copier.py configuration_file.xml\"\n
Xml - file must be in Utf-8 encoding!
Example of configuration file:
<?xml version="1.0" encoding="utf-8"?>
<files>
<file id="0">
<filename>bash</filename>
<oldpath>/bin/</oldpath>
<newpath>/media/</newpath>
</file>
<file id="1">
<filename>Testfile.txt</filename>
<oldpath>/tmp/</oldpath>
<newpath>/home/User/</newpath>
</file>
</files>
"""

def break_programm(msg, code = 0):
	print(msg)
	sys.exit(code)
	
def copy_by_config(path_to_config):
	try:
		xml_parser = xml_tree.XMLParser(encoding = "utf-8")
		tree = xml_tree.parse(path_to_config, xml_parser)
	except IOError as IOErr:
		break_programm(IOErr, 1)
	except SyntaxError as pErr:
		break_programm("XML Parse error in \"%s\":\n%s" % (path_to_config, pErr), 1)
	
	
	#		Обход xml-файла		#
	
	root = tree.getroot()
	error_counter = copied_files = 0 
	for file in  root:
		old_path = join(file.find("oldpath").text, file.find("filename").text)
		if not exists(old_path):
			print("Err - no such file \"%s\" %s" % (old_path, file.attrib))
			error_counter += 1
			continue
		new_path = join(file.find("newpath").text, file.find("filename").text)
		
		#		Защита от затирания файла с таким же именем		#
		if exists(new_path):
			number = 1
			fname, fext = splitext(new_path)
			while( exists(fname + str(number) + fext) ):
				number += 1
			new_path = fname + str(number) + fext
		try:
			shutil.copyfile(old_path, new_path)
		except IOError as IOErr:
			print("Copying problem with file \"%s\" %s" % (new_path, file.attrib))
			error_counter += 1
			continue
		copied_files += 1
	print("Copied files: %d\nErrors: %d" % ( copied_files, error_counter))

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		break_programm(manual, 1)
	copy_by_config(sys.argv[1])